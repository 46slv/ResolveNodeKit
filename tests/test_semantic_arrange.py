import unittest

from resolve_node_kit.fusion import (
    ArrangeDialogState,
    ArrangeError,
    FusionHostError,
    SemanticEdge,
    SemanticError,
    arrange_comp,
    build_snapshot,
    plan_layout,
    resolve_arrange_scope,
)


class MockOutput:
    def __init__(self, tool):
        self.tool = tool

    def GetTool(self):
        return self.tool


class MockInput:
    def __init__(self, source, input_id):
        self.output = MockOutput(source)
        self.input_id = input_id

    def GetConnectedOutput(self):
        return self.output

    def GetAttrs(self):
        return {"INPS_ID": self.input_id, "INPN_Name": self.input_id}


class MockTool:
    def __init__(self, name, reg_id="Mock", parent=None):
        self.Name = name
        self.inputs = []
        self.parent = parent
        self.children = []
        self.reg_id = reg_id
        if parent is not None:
            parent.children.append(self)

    @property
    def ParentTool(self):
        return self.parent

    def GetChildrenList(self):
        return list(self.children)

    def GetInputList(self):
        return list(self.inputs)

    def GetAttrs(self):
        result = {"TOOLS_Name": self.Name, "TOOLS_RegID": self.reg_id}
        if self.parent is not None:
            result["TOOLH_GroupParent"] = self.parent
        return result


class MockFlow:
    def __init__(self, positions):
        self.positions = dict(positions)
        self.calls = 0

    def GetPosTable(self, tool):
        return {1: self.positions[tool.Name][0], 2: self.positions[tool.Name][1]}

    def SetPos(self, tool, x, y):
        self.calls += 1
        self.positions[tool.Name] = (float(x), float(y))
        return True


class MockComp:
    def __init__(self, root_tools, flow, selected=()):
        self.tools = list(root_tools)
        self.CurrentFrame = type("Frame", (), {"FlowView": flow})()
        self.undo = []
        self.selected = set(selected)

    def GetToolList(self, selected=False):
        if not selected:
            return list(self.tools)
        found = []
        queue = list(self.tools)
        while queue:
            tool = queue.pop(0)
            if tool.Name in self.selected:
                found.append(tool)
            queue.extend(tool.children)
        return found

    def FindTool(self, name):
        queue = list(self.tools)
        while queue:
            tool = queue.pop(0)
            if tool.Name == name:
                return tool
            queue.extend(tool.children)
        return None

    def StartUndo(self, name):
        self.undo.append(("start", name))

    def EndUndo(self, keep):
        self.undo.append(("end", bool(keep)))


def connect(source, target, input_id):
    target.inputs.append(MockInput(source, input_id))


def merge_rail_snapshot():
    names = ["BG", "A", "M1", "B", "M2", "C", "M3", "Out"]
    edges = [
        SemanticEdge("BG", "M1", "background"),
        SemanticEdge("A", "M1", "foreground"),
        SemanticEdge("M1", "M2", "background"),
        SemanticEdge("B", "M2", "foreground"),
        SemanticEdge("M2", "M3", "background"),
        SemanticEdge("C", "M3", "foreground"),
        SemanticEdge("M3", "Out", "other"),
    ]
    reg_ids = {"M1": "Merge", "M2": "Merge", "M3": "Merge"}
    return build_snapshot(names, edges, reg_ids, {}, set())


class SemanticPlannerTests(unittest.TestCase):
    def test_f1_merge_rail_horizontal_branches_above(self):
        layout = plan_layout(merge_rail_snapshot())
        scope = layout.scopes[None]
        rows = {scope.placements[n].row for n in ("M1", "M2", "M3")}
        self.assertEqual(rows, {0})
        cols = [scope.placements[n].column for n in ("BG", "M1", "M2", "M3", "Out")]
        self.assertEqual(cols, sorted(cols))
        for branch, receiver in (("A", "M1"), ("B", "M2"), ("C", "M3")):
            self.assertEqual(scope.placements[branch].column, scope.placements[receiver].column)
            self.assertLess(scope.placements[branch].row, scope.placements[receiver].row)
        diag = layout.diagnostics
        self.assertEqual(diag["overlap_count"], 0)
        self.assertEqual(diag["backbone_order_violation_count"], 0)
        self.assertEqual(diag["branch_lane_violation_count"], 0)
        self.assertEqual(diag["avoidable_diagonal_edge_count"], 0)
        self.assertEqual(len(scope.merge_runs), 1)

    def test_f1_second_plan_identical(self):
        first = plan_layout(merge_rail_snapshot())
        second = plan_layout(merge_rail_snapshot())
        self.assertEqual(first.scopes[None].placements, second.scopes[None].placements)

    def test_f2_branch_clearance_widens_merge_gaps(self):
        layout = plan_layout(merge_rail_snapshot())
        scope = layout.scopes[None]
        reasons = set(scope.gap_reasons.values())
        self.assertIn("BRANCH_CLEARANCE", reasons)
        gaps = [
            scope.placements[b].column - scope.placements[a].column
            for a, b in (("M1", "M2"), ("M2", "M3"))
        ]
        for gap in gaps:
            self.assertIsInstance(gap, int)
            self.assertGreaterEqual(gap, 3)
        self.assertGreater(max(gaps), 3)


class SemanticGroupTests(unittest.TestCase):
    def test_f3_child_group_feeding_rail(self):
        names = ["BG", "M1", "GA", "M2", "Out", "GIn", "GM"]
        edges = [
            SemanticEdge("BG", "M1", "background"),
            SemanticEdge("GA", "M1", "foreground"),
            SemanticEdge("M1", "M2", "background"),
            SemanticEdge("M2", "Out", "other"),
            SemanticEdge("GIn", "GM", "other"),
        ]
        parents = {"GIn": "GA", "GM": "GA"}
        reg_ids = {"M1": "Merge", "M2": "Merge", "GA": "GroupOperator", "GM": "Merge"}
        snapshot = build_snapshot(names, edges, reg_ids, parents, {"GA"})
        layout = plan_layout(snapshot)
        root = layout.scopes[None]
        self.assertIn("GA", root.placements)
        self.assertEqual(root.placements["GA"].column, root.placements["M1"].column)
        self.assertLess(root.placements["GA"].row, root.placements["M1"].row)
        inner = layout.scopes["GA"]
        self.assertEqual(
            {inner.placements["GIn"].row, inner.placements["GM"].row}, {0}
        )
        self.assertEqual(layout.diagnostics["overlap_count"], 0)
        self.assertEqual(layout.diagnostics["avoidable_diagonal_edge_count"], 0)
        self.assertEqual(layout.diagnostics["scope_count"], 2)

    def test_f4_nested_group_internal_rail(self):
        names = ["BG", "M1", "Out", "GA", "A1", "A2", "GB", "B1", "B2"]
        edges = [
            SemanticEdge("BG", "M1", "background"),
            SemanticEdge("GA", "M1", "foreground"),
            SemanticEdge("M1", "Out", "other"),
            SemanticEdge("A1", "A2", "background"),
            SemanticEdge("GB", "A2", "foreground"),
            SemanticEdge("B1", "B2", "background"),
        ]
        parents = {"A1": "GA", "A2": "GA", "GB": "GA", "B1": "GB", "B2": "GB"}
        reg_ids = {
            "M1": "Merge", "GA": "GroupOperator", "A1": "Merge",
            "A2": "Merge", "GB": "GroupOperator",
        }
        snapshot = build_snapshot(names, edges, reg_ids, parents, {"GA", "GB"})
        layout = plan_layout(snapshot)
        diag = layout.diagnostics
        self.assertEqual(diag["scope_count"], 3)
        self.assertEqual(diag["max_group_depth"], 2)
        inner_a = layout.scopes["GA"]
        self.assertEqual(inner_a.placements["A1"].row, inner_a.placements["A2"].row)
        self.assertLess(
            inner_a.placements["A1"].column, inner_a.placements["A2"].column
        )
        inner_b = layout.scopes["GB"]
        self.assertEqual(inner_b.placements["B1"].row, inner_b.placements["B2"].row)
        self.assertEqual(diag["overlap_count"], 0)
        self.assertEqual(diag["avoidable_diagonal_edge_count"], 0)

    def test_f6_disconnected_component_in_peripheral_lane(self):
        snapshot = merge_rail_snapshot()
        names = list(snapshot.nodes) + ["Iso"]
        layout = plan_layout(
            build_snapshot(
                names, list(snapshot.edges),
                {"M1": "Merge", "M2": "Merge", "M3": "Merge"}, {}, set(),
            )
        )
        root = layout.scopes[None]
        self.assertIn("Iso", root.placements)
        self.assertGreater(root.placements["Iso"].row, 0)
        self.assertEqual(layout.diagnostics["overlap_count"], 0)

    def test_vertical_reduction_column(self):
        names = ["BG", "M1", "Out", "V1", "V2", "S1", "S2"]
        edges = [
            SemanticEdge("BG", "M1", "background"),
            SemanticEdge("V2", "M1", "foreground"),
            SemanticEdge("M1", "Out", "other"),
            SemanticEdge("V1", "V2", "background"),
            SemanticEdge("S1", "V1", "foreground"),
            SemanticEdge("S2", "V2", "foreground"),
        ]
        reg_ids = {"M1": "Merge", "V1": "Merge", "V2": "Merge"}
        layout = plan_layout(build_snapshot(names, edges, reg_ids, {}, set()))
        root = layout.scopes[None]
        self.assertEqual(root.placements["V1"].column, root.placements["V2"].column)
        self.assertLess(root.placements["V1"].row, root.placements["V2"].row)
        self.assertEqual(root.placements["V2"].row, root.placements["M1"].row)
        self.assertEqual(root.placements["S1"].row, root.placements["V1"].row)
        self.assertEqual(root.placements["S2"].row, root.placements["V2"].row)
        self.assertEqual(layout.diagnostics["avoidable_diagonal_edge_count"], 0)

    def test_f9_fixed_point_under_host_like_offsets(self):
        first = plan_layout(merge_rail_snapshot())
        second = plan_layout(merge_rail_snapshot())
        for scope_id in first.scopes:
            self.assertEqual(
                first.scopes[scope_id].placements, second.scopes[scope_id].placements
            )
        self.assertLessEqual(second.diagnostics["fixed_point_iterations"], 16)

    def test_snapshot_rejects_unknown_edge(self):
        with self.assertRaises(SemanticError):
            build_snapshot(["A"], [SemanticEdge("A", "Ghost", "other")], {}, {}, set())

    def test_snapshot_rejects_cycle(self):
        snapshot = build_snapshot(
            ["A", "B"],
            [SemanticEdge("A", "B", "other"), SemanticEdge("B", "A", "other")],
            {}, {}, set(),
        )
        with self.assertRaises(SemanticError):
            plan_layout(snapshot)


class ArrangeDialogTests(unittest.TestCase):
    def test_defaults_are_off(self):
        state = ArrangeDialogState()
        self.assertFalse(state.include_unselected)
        self.assertFalse(state.ungroup)

    def test_cancel_yields_none(self):
        self.assertIsNone(ArrangeDialogState.from_askuser(None))
        self.assertIsNone(ArrangeDialogState.from_askuser(False))

    def test_checkbox_values_parse(self):
        state = ArrangeDialogState.from_askuser({"IncludeUnselected": 1, "UngroupFirst": 0})
        assert state is not None
        self.assertTrue(state.include_unselected)
        self.assertFalse(state.ungroup)


class ArrangeScopeTests(unittest.TestCase):
    def test_empty_selection_fails_closed(self):
        with self.assertRaises(ArrangeError):
            resolve_arrange_scope(["A", "B"], [], False)

    def test_selection_only_keeps_explicit_set(self):
        self.assertEqual(
            resolve_arrange_scope(["A", "B", "C"], ["B"], False), {"B"}
        )

    def test_whole_comp_requires_explicit_flag(self):
        self.assertEqual(
            resolve_arrange_scope(["A", "B"], [], True), {"A", "B"}
        )


def serial_comp(names, kinds=None, positions=None):
    tools = {}
    for name in names:
        reg = (kinds or {}).get(name, "Mock")
        tools[name] = MockTool(name, reg)
    order = list(names)
    for source, target in zip(order, order[1:]):
        connect(tools[source], tools[target], "Input")
    if positions is None:
        positions = {name: (float(i), 0.0) for i, name in enumerate(names)}
    flow = MockFlow(positions)
    return MockComp(list(tools.values()), flow), flow, tools


class ArrangeCompTests(unittest.TestCase):
    def test_selection_only_moves_selected(self):
        comp, flow, tools = serial_comp(["A", "B", "C", "D"])
        before_c = flow.positions["C"]
        before_d = flow.positions["D"]
        result = arrange_comp(comp, include_unselected=False, selected_names={"A", "B"})
        self.assertEqual(result["arranged_count"], 2)
        self.assertEqual(flow.positions["C"], before_c)
        self.assertEqual(flow.positions["D"], before_d)
        self.assertEqual(comp.undo[-1], ("end", True))

    def test_selection_reads_host_selection(self):
        comp, flow, tools = serial_comp(["A", "B", "C"])
        comp.selected = {"C"}
        result = arrange_comp(comp, include_unselected=False)
        self.assertEqual(result["arranged_count"], 1)

    def test_empty_selection_writes_nothing(self):
        comp, flow, tools = serial_comp(["A", "B"])
        before = dict(flow.positions)
        with self.assertRaises(FusionHostError):
            arrange_comp(comp, include_unselected=False, selected_names=set())
        self.assertEqual(flow.calls, 0)
        self.assertEqual(flow.positions, before)
        self.assertEqual(comp.undo, [])

    def test_whole_comp_arranges_all(self):
        comp, flow, tools = serial_comp(["A", "B", "C"])
        result = arrange_comp(comp, include_unselected=True)
        self.assertEqual(result["arranged_count"], 3)
        self.assertEqual(result["diagnostics"]["overlap_count"], 0)

    def test_ungroup_is_fail_closed(self):
        comp, flow, tools = serial_comp(["A", "B"])
        before = dict(flow.positions)
        with self.assertRaises(FusionHostError):
            arrange_comp(comp, include_unselected=True, ungroup=True)
        self.assertEqual(flow.calls, 0)
        self.assertEqual(flow.positions, before)
        self.assertEqual(comp.undo, [])

    def test_second_run_is_stable(self):
        comp, flow, tools = serial_comp(
            ["BG", "M1", "M2", "Out"],
            {"M1": "Merge", "M2": "Merge"},
        )
        connect(tools["BG"], tools["M1"], "Background")
        first = arrange_comp(comp, include_unselected=True)
        self.assertGreater(first["moved_count"], 0)
        second = arrange_comp(comp, include_unselected=True)
        self.assertEqual(second["moved_count"], 0)

    def test_host_grid_alignment(self):
        comp, flow, tools = serial_comp(["A", "B", "C"])
        arrange_comp(comp, include_unselected=True)
        for name, (x, y) in flow.positions.items():
            self.assertAlmostEqual(x / 0.5, round(x / 0.5), places=6)
            self.assertAlmostEqual(y, round(y), places=6)

    def test_selected_group_brings_subtree_only(self):
        inner_a = MockTool("InnerA")
        inner_b = MockTool("InnerB")
        group = MockTool("G", "GroupOperator")
        inner_a.parent = group
        inner_b.parent = group
        group.children = [inner_a, inner_b]
        sibling = MockTool("Sibling")
        connect(inner_a, inner_b, "Input")
        positions = {"G": (0.0, 0.0), "InnerA": (5.0, 5.0), "InnerB": (9.0, 1.0), "Sibling": (2.0, 2.0)}
        flow = MockFlow(positions)
        comp = MockComp([group, sibling], flow)
        result = arrange_comp(comp, include_unselected=False, selected_names={"G"})
        self.assertEqual(result["arranged_count"], 3)
        self.assertEqual(flow.positions["Sibling"], (2.0, 2.0))

    def test_selected_child_does_not_move_parent(self):
        inner = MockTool("Inner")
        group = MockTool("G", "GroupOperator")
        inner.parent = group
        group.children = [inner]
        positions = {"G": (0.0, 0.0), "Inner": (5.0, 5.0)}
        flow = MockFlow(positions)
        comp = MockComp([group], flow)
        arrange_comp(comp, include_unselected=False, selected_names={"Inner"})
        self.assertEqual(flow.positions["G"], (0.0, 0.0))


class ArrangeAnchorTests(unittest.TestCase):
    def _branch_comp(self):
        bg = MockTool("BG")
        a = MockTool("A")
        m1 = MockTool("M1", "Merge")
        b = MockTool("B")
        m2 = MockTool("M2", "Merge")
        out = MockTool("Out")
        connect(bg, m1, "Background")
        connect(a, m1, "Foreground")
        connect(m1, m2, "Background")
        connect(b, m2, "Foreground")
        connect(m2, out, "Input")
        positions = {
            "BG": (-0.499, -0.49),
            "A": (-0.499, -0.49),
            "M1": (-0.499, -0.49),
            "B": (-0.499, -0.49),
            "M2": (-0.499, -0.49),
            "Out": (3.5, 1.009),
        }
        flow = MockFlow(positions)
        return MockComp([bg, a, m1, b, m2, out], flow), flow

    def test_branches_above_do_not_drag_anchor(self):
        comp, flow = self._branch_comp()
        first = arrange_comp(comp, include_unselected=True)
        self.assertGreater(first["moved_count"], 0)
        post_run1 = dict(flow.positions)
        second = arrange_comp(comp, include_unselected=True)
        self.assertEqual(second["moved_count"], 0)
        self.assertEqual(flow.positions, post_run1)
        third = arrange_comp(comp, include_unselected=True)
        self.assertEqual(third["moved_count"], 0)
        self.assertEqual(flow.positions, post_run1)

    def test_backbone_row_stable_across_runs(self):
        comp, flow = self._branch_comp()
        arrange_comp(comp, include_unselected=True)
        rows_run1 = (flow.positions["M1"][1], flow.positions["M2"][1])
        arrange_comp(comp, include_unselected=True)
        self.assertEqual((flow.positions["M1"][1], flow.positions["M2"][1]), rows_run1)


class ArrangeSelectionReadTests(unittest.TestCase):
    def test_host_shape_true_filters_selection(self):
        comp, flow, tools = serial_comp(["A", "B", "C"])
        comp.selected = {"B"}
        self.assertEqual(
            sorted(t.Name for t in comp.GetToolList(True)),
            ["B"],
        )

    def test_no_selection_api_fails_closed(self):
        tools = [MockTool("A"), MockTool("B")]

        class NoSelectComp(MockComp):
            def GetToolList(self):
                return list(self.tools)

        flow = MockFlow({"A": (0.0, 0.0), "B": (1.0, 0.0)})
        comp = NoSelectComp(tools, flow)
        before = dict(flow.positions)
        with self.assertRaises(FusionHostError):
            arrange_comp(comp, include_unselected=False)
        self.assertEqual(flow.calls, 0)
        self.assertEqual(flow.positions, before)
        self.assertEqual(comp.undo, [])


class ArrangeDialogInvokeTests(unittest.TestCase):
    def test_first_shape_accepted(self):
        from resolve_node_kit.fusion.dialog import ask_arrange_options
        calls = []

        def ask(title, controls):
            calls.append((title, controls))
            return {"LABEL_A": 1, "LABEL_B": 0}

        logged = []
        state = ask_arrange_options(ask, "T", "LABEL_A", "LABEL_B", log=logged.append)
        assert state is not None
        self.assertTrue(state.include_unselected)
        self.assertFalse(state.ungroup)
        self.assertEqual(len(calls), 1)
        self.assertTrue(logged)

    def test_none_then_dict_uses_second_shape(self):
        from resolve_node_kit.fusion.dialog import ask_arrange_options
        calls = []

        def ask(title, controls):
            calls.append(controls)
            if len(calls) == 1:
                return None
            return {"LABEL_B": 1}

        state = ask_arrange_options(ask, "T", "LABEL_A", "LABEL_B")
        assert state is not None
        self.assertFalse(state.include_unselected)
        self.assertTrue(state.ungroup)
        self.assertEqual(len(calls), 2)

    def test_all_none_means_cancel(self):
        from resolve_node_kit.fusion.dialog import ask_arrange_options
        calls = []

        def ask(title, controls):
            calls.append(controls)
            return None

        self.assertIsNone(ask_arrange_options(ask, "T", "LABEL_A", "LABEL_B"))
        self.assertEqual(len(calls), 2)

    def test_exception_then_dict(self):
        from resolve_node_kit.fusion.dialog import ask_arrange_options
        calls = []

        def ask(title, controls):
            calls.append(controls)
            if len(calls) == 1:
                raise RuntimeError("bad shape")
            return {"LABEL_A": 0, "LABEL_B": 0}

        state = ask_arrange_options(ask, "T", "LABEL_A", "LABEL_B")
        assert state is not None
        self.assertFalse(state.include_unselected)
        self.assertFalse(state.ungroup)
        self.assertEqual(len(calls), 2)


class ArrangeHostileApiTests(unittest.TestCase):
    def test_none_input_list_is_tolerated(self):
        a = MockTool("A")
        b = MockTool("B")
        b.GetInputList = None
        connect(a, b, "Input")
        flow = MockFlow({"A": (0.0, 0.0), "B": (5.0, 5.0)})
        comp = MockComp([a, b], flow)
        result = arrange_comp(comp, include_unselected=True)
        self.assertEqual(result["arranged_count"], 2)
        self.assertEqual(result["diagnostics"]["overlap_count"], 0)

    def test_none_returning_input_list_is_tolerated(self):
        a = MockTool("A")
        b = MockTool("B")

        def no_inputs():
            return None

        b.GetInputList = no_inputs
        connect(a, b, "Input")
        flow = MockFlow({"A": (0.0, 0.0), "B": (5.0, 5.0)})
        comp = MockComp([a, b], flow)
        result = arrange_comp(comp, include_unselected=True)
        self.assertEqual(result["arranged_count"], 2)

    def test_progress_phases_reported(self):
        comp, flow, tools = serial_comp(["A", "B", "C"])
        phases = []
        arrange_comp(comp, include_unselected=True, progress=phases.append)
        joined = " ".join(phases)
        for marker in ("snapshot", "plan", "writes", "readback", "verify"):
            self.assertIn(marker, joined)
