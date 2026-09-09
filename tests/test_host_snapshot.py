import json
import unittest

from resolve_node_kit.fusion.host_snapshot import (
    HostSnapshotError,
    build_host_processing_snapshot,
)
from resolve_node_kit.fusion.processing_snapshot import SnapshotState


class _Port:
    def __init__(self, attrs, *, tool=None, output=None, inputs=None, log=None):
        self._attrs = dict(attrs)
        self._tool = tool
        self._output = output
        self._inputs = list(inputs or [])
        self._log = log if log is not None else []

    def GetAttrs(self):
        self._log.append("GetAttrs")
        return dict(self._attrs)

    def GetTool(self):
        self._log.append("GetTool")
        return self._tool

    def GetConnectedOutput(self):
        self._log.append("GetConnectedOutput")
        return self._output

    def GetConnectedInputs(self):
        self._log.append("GetConnectedInputs")
        return list(self._inputs)


class _Tool:
    def __init__(self, name, reg_id, *, parent=None, children=None, log=None):
        self.Name = name
        self.ID = reg_id
        self.ParentTool = parent
        self.children = list(children or [])
        self.inputs = []
        self.outputs = []
        self._log = log if log is not None else []

    def GetAttrs(self):
        self._log.append(f"{self.Name}.GetAttrs")
        return {"TOOLS_Name": self.Name, "TOOLS_RegID": self.ID, "TOOLB_Example": True}

    def GetChildrenList(self):
        self._log.append(f"{self.Name}.GetChildrenList")
        return list(self.children)

    def GetInputList(self):
        self._log.append(f"{self.Name}.GetInputList")
        return list(self.inputs)

    def GetOutputList(self):
        self._log.append(f"{self.Name}.GetOutputList")
        return list(self.outputs)

    def SetPos(self, *_args):
        raise AssertionError("adapter must not write positions")

    def LoadSettings(self, *_args):
        raise AssertionError("adapter must not load settings")

    def Undo(self, *_args):
        raise AssertionError("adapter must not call Undo")


class _Comp:
    def __init__(self, tools, log=None):
        self.tools = list(tools)
        self._log = log if log is not None else []

    def GetToolList(self):
        self._log.append("GetToolList")
        return list(self.tools)

    def Save(self, *_args):
        raise AssertionError("adapter must not save")


class _Flow:
    def __init__(self, positions, log=None):
        self.positions = dict(positions)
        self._log = log if log is not None else []

    def GetPosTable(self, tool):
        self._log.append(f"GetPosTable:{tool.Name}")
        return {1: self.positions[tool.Name][0], 2: self.positions[tool.Name][1]}

    def SetPos(self, *_args):
        raise AssertionError("adapter must not write positions")


def _connected_fixture():
    log = []
    group = _Tool("Group", "GroupOperator", log=log)
    source = _Tool("Source", "Loader", parent=group, log=log)
    target = _Tool("Target", "Merge", parent=group, log=log)
    group.children = [source, target]
    output = _Port({"OUTS_ID": "Output", "OUTS_Name": "Output"}, tool=source, log=log)
    target_input = _Port(
        {"INPS_ID": "Foreground", "INPN_Name": "Foreground"},
        tool=target,
        output=output,
        log=log,
    )
    output._inputs = [target_input]
    source.outputs = [output]
    target.inputs = [target_input]
    comp = _Comp([group], log=log)
    flow = _Flow({"Group": (0, 0), "Source": (10, 20), "Target": (30, 40)}, log=log)
    return comp, flow, log


class HostSnapshotTests(unittest.TestCase):
    def test_read_only_connected_snapshot_preserves_both_endpoint_ids(self):
        comp, flow, log = _connected_fixture()
        snapshot = build_host_processing_snapshot(comp, flow)
        edge = snapshot.connections[0]
        self.assertEqual((edge.source, edge.target), ("Source", "Target"))
        self.assertEqual((edge.source_output_id, edge.target_input_id), ("Output", "Foreground"))
        self.assertEqual(edge.state, SnapshotState.COMPLETE)
        self.assertEqual(snapshot.nodes["Target"].inputs[0], edge)
        self.assertEqual(snapshot.nodes["Source"].position.value, [10.0, 20.0])
        self.assertEqual(snapshot.fields["ports"].state, SnapshotState.COMPLETE)
        json.dumps(snapshot.as_dict(), sort_keys=True)
        forbidden = ("SetPos", "LoadSettings", "Undo", "Save")
        self.assertFalse(any(any(item in call for item in forbidden) for call in log))

    def test_missing_port_identity_is_explicit_and_not_dropped(self):
        log = []
        source = _Tool("Source", "Loader", log=log)
        target = _Tool("Target", "Merge", log=log)
        output = _Port({}, tool=source, log=log)
        target_input = _Port({"INPS_ID": "Foreground"}, tool=target, output=output, log=log)
        output._inputs = [target_input]
        source.outputs = [output]
        target.inputs = [target_input]
        snapshot = build_host_processing_snapshot(
            _Comp([source, target], log=log),
            _Flow({"Source": (0, 0), "Target": (1, 1)}, log=log),
        )
        self.assertEqual(len(snapshot.connections), 1)
        self.assertEqual(snapshot.connections[0].state, SnapshotState.UNSUPPORTED)
        self.assertEqual(snapshot.connections[0].source_output_id, "")
        self.assertIn("source_output_id unavailable", snapshot.connections[0].detail or "")
        self.assertEqual(snapshot.fields["ports"].state, SnapshotState.UNSUPPORTED)

    def test_connection_to_undiscovered_tool_is_not_declared_complete(self):
        log = []
        source = _Tool("Source", "Loader", log=log)
        external = _Tool("External", "Merge", log=log)
        output = _Port({"OUTS_ID": "Output"}, tool=source, log=log)
        external_input = _Port({"INPS_ID": "Foreground"}, tool=external, log=log)
        output._inputs = [external_input]
        source.outputs = [output]
        # The discovered comp contains Source only; External is a host object
        # returned by a connection API but not a discovered graph node.
        snapshot = build_host_processing_snapshot(_Comp([source], log=log))
        self.assertEqual(len(snapshot.connections), 1)
        self.assertEqual(snapshot.connections[0].state, SnapshotState.UNSUPPORTED)
        self.assertIn("was not discovered", snapshot.connections[0].detail or "")

    def test_group_child_discovery_missing_is_fail_closed(self):
        group = _Tool("Group", "GroupOperator")
        group.GetChildrenList = None
        with self.assertRaises(HostSnapshotError):
            build_host_processing_snapshot(_Comp([group]))

    def test_duplicate_names_are_fail_closed(self):
        first = _Tool("Same", "Loader")
        second = _Tool("Same", "Merge")
        with self.assertRaises(HostSnapshotError):
            build_host_processing_snapshot(_Comp([first, second]))

    def test_group_cycle_is_fail_closed(self):
        first = _Tool("First", "GroupOperator")
        second = _Tool("Second", "GroupOperator", parent=first)
        first.ParentTool = second
        first.children = [second]
        second.children = [first]
        with self.assertRaises(HostSnapshotError):
            build_host_processing_snapshot(_Comp([first]))

    def test_missing_surface_is_unsupported_not_empty_complete(self):
        source = _Tool("Source", "Loader")
        source.GetOutputList = None
        snapshot = build_host_processing_snapshot(_Comp([source]))
        self.assertEqual(snapshot.fields["ports"].state, SnapshotState.UNSUPPORTED)
        self.assertEqual(snapshot.fields["parameters"].state, SnapshotState.UNSUPPORTED)
        self.assertEqual(snapshot.fields["keyframes"].state, SnapshotState.UNSUPPORTED)
        self.assertEqual(snapshot.fields["expressions"].state, SnapshotState.UNSUPPORTED)
        self.assertEqual(snapshot.fields["instances"].state, SnapshotState.UNSUPPORTED)
        self.assertEqual(snapshot.fields["media"].state, SnapshotState.UNSUPPORTED)
        self.assertEqual(snapshot.fields["time_range"].state, SnapshotState.UNSUPPORTED)


if __name__ == "__main__":
    unittest.main()
