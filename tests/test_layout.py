import unittest

from resolve_node_kit.core import Edge, LayoutConfig, LayoutError, layout_graph


class LayoutTests(unittest.TestCase):
    def test_serial_chain_is_horizontal_and_monotonic(self):
        positions = layout_graph(["A", "B", "C"], [Edge("A", "B"), Edge("B", "C")])
        self.assertEqual(positions["A"][1], positions["B"][1])
        self.assertEqual(positions["B"][1], positions["C"][1])
        self.assertLess(positions["A"][0], positions["B"][0])
        self.assertLess(positions["B"][0], positions["C"][0])

    def test_merge_sources_do_not_overlap(self):
        positions = layout_graph(["BG", "FG", "Merge"], [Edge("BG", "Merge", "background"), Edge("FG", "Merge", "foreground")])
        self.assertNotEqual(positions["BG"], positions["FG"])
        self.assertEqual(positions["BG"][0], positions["FG"][0])

    def test_isolated_node_is_reserved_as_component(self):
        positions = layout_graph(["A", "B", "Loose"], [Edge("A", "B")])
        self.assertEqual(len(set(positions.values())), 3)

    def test_disconnected_components_do_not_overlap(self):
        positions = layout_graph(["A", "B", "C", "D"], [Edge("A", "B"), Edge("C", "D")])
        self.assertEqual(len(set(positions.values())), 4)

    def test_repeated_layout_is_stable(self):
        nodes = ["A", "B", "C", "D"]
        edges = [Edge("A", "C"), Edge("B", "C"), Edge("C", "D")]
        first = layout_graph(nodes, edges, original_positions={n: (0.0, float(i)) for i, n in enumerate(nodes)})
        second = layout_graph(nodes, edges, original_positions=first)
        self.assertEqual(first, second)

    def test_cycle_fails_closed(self):
        with self.assertRaises(LayoutError):
            layout_graph(["A", "B"], [Edge("A", "B"), Edge("B", "A")])

    def test_large_chain_is_iterative(self):
        count = 1110
        nodes = [f"N{i:04d}" for i in range(count)]
        edges = [Edge(nodes[i], nodes[i + 1]) for i in range(count - 1)]
        result = layout_graph(nodes, edges, config=LayoutConfig(spacing_x=2.0))
        self.assertEqual(len(result), count)
        self.assertEqual(result[nodes[-1]][0], (count - 1) * 2.0)


if __name__ == "__main__":
    unittest.main()
