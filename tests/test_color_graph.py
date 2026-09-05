import unittest

from resolve_node_kit.color import ColorHostError, get_node_graph, probe_resolve_graphs, snapshot_graph


class MockGraph:
    def __init__(self, count=2): self.count = count
    def GetNumNodes(self): return self.count
    def GetNodeLabel(self, index): return f"Node {index}"
    def GetLUT(self, index): return "" if index == 1 else "Film Looks/Test.cube"
    def GetNodeCacheMode(self, index): return -1
    def GetToolsInNode(self, index): return [] if index == 1 else ["OFX"]


class MockTimelineItem:
    def __init__(self, graph): self.graph = graph
    def GetNodeGraph(self): return self.graph


class MockTimeline:
    def __init__(self, timeline_graph, item): self.timeline_graph, self.item = timeline_graph, item
    def GetNodeGraph(self): return self.timeline_graph
    def GetCurrentVideoItem(self): return self.item


class MockProject:
    def __init__(self, timeline): self.timeline = timeline
    def GetCurrentTimeline(self): return self.timeline


class MockManager:
    def __init__(self, project): self.project = project
    def GetCurrentProject(self): return self.project


class MockResolve:
    def __init__(self, project): self.project = project
    def GetProjectManager(self): return MockManager(self.project)


class ColorGraphTests(unittest.TestCase):
    def test_snapshot_uses_one_based_node_indices(self):
        snapshot = snapshot_graph(MockGraph(2))
        self.assertEqual(snapshot.node_count, 2)
        self.assertEqual([node.index for node in snapshot.nodes], [1, 2])
        self.assertEqual(snapshot.nodes[1].label, "Node 2")
        self.assertEqual(snapshot.nodes[1].tool_count, 1)

    def test_missing_optional_methods_are_tolerated(self):
        class CountOnly:
            def GetNumNodes(self): return 1
        snapshot = snapshot_graph(CountOnly())
        self.assertIsNone(snapshot.nodes[0].label)
        self.assertIsNone(snapshot.nodes[0].tool_count)

    def test_missing_get_num_nodes_fails_closed(self):
        with self.assertRaises(ColorHostError):
            snapshot_graph(object())

    def test_get_node_graph_can_be_absent(self):
        self.assertIsNone(get_node_graph(object()))

    def test_probe_discovers_timeline_and_current_item_graphs(self):
        timeline_graph = MockGraph(1)
        item_graph = MockGraph(3)
        resolve = MockResolve(MockProject(MockTimeline(timeline_graph, MockTimelineItem(item_graph))))
        result = probe_resolve_graphs(resolve)
        self.assertEqual(result["timeline"].node_count, 1)
        self.assertEqual(result["current_item"].node_count, 3)


if __name__ == "__main__":
    unittest.main()
