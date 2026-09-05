from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class ColorHostError(RuntimeError):
    pass


@dataclass(frozen=True)
class ColorNodeSnapshot:
    index: int
    label: str | None
    lut: str | None
    cache_mode: Any
    tool_count: int | None


@dataclass(frozen=True)
class ColorGraphSnapshot:
    node_count: int
    nodes: tuple[ColorNodeSnapshot, ...]


def _optional_call(obj: Any, name: str, *args: Any) -> Any:
    method = getattr(obj, name, None)
    if not callable(method):
        return None
    try:
        return method(*args)
    except Exception:
        return None


def get_node_graph(scope_obj: Any, layer_index: int | None = None) -> Any:
    getter = getattr(scope_obj, "GetNodeGraph", None)
    if not callable(getter):
        return None
    try:
        return getter() if layer_index is None else getter(layer_index)
    except Exception:
        return None


def snapshot_graph(graph: Any) -> ColorGraphSnapshot:
    get_count = getattr(graph, "GetNumNodes", None)
    if not callable(get_count):
        raise ColorHostError("Color Graph.GetNumNodes is unavailable")
    try:
        node_count = int(get_count())
    except Exception as exc:
        raise ColorHostError(f"Color Graph.GetNumNodes failed: {exc}") from exc
    if node_count < 0:
        raise ColorHostError(f"invalid Color node count: {node_count}")

    nodes: list[ColorNodeSnapshot] = []
    for index in range(1, node_count + 1):
        tools = _optional_call(graph, "GetToolsInNode", index)
        try:
            tool_count = len(tools) if tools is not None else None
        except Exception:
            tool_count = None
        nodes.append(
            ColorNodeSnapshot(
                index=index,
                label=_optional_call(graph, "GetNodeLabel", index),
                lut=_optional_call(graph, "GetLUT", index),
                cache_mode=_optional_call(graph, "GetNodeCacheMode", index),
                tool_count=tool_count,
            )
        )
    return ColorGraphSnapshot(node_count=node_count, nodes=tuple(nodes))


def probe_resolve_graphs(resolve_app: Any) -> dict[str, ColorGraphSnapshot | None]:
    """Best-effort, read-only graph discovery for the current Resolve context."""
    result: dict[str, ColorGraphSnapshot | None] = {"timeline": None, "current_item": None}
    manager = _optional_call(resolve_app, "GetProjectManager")
    project = _optional_call(manager, "GetCurrentProject") if manager is not None else None
    timeline = _optional_call(project, "GetCurrentTimeline") if project is not None else None
    if timeline is None:
        return result

    timeline_graph = get_node_graph(timeline)
    if timeline_graph:
        try:
            result["timeline"] = snapshot_graph(timeline_graph)
        except ColorHostError:
            pass

    current_item = _optional_call(timeline, "GetCurrentVideoItem")
    if current_item is not None:
        item_graph = get_node_graph(current_item)
        if item_graph:
            try:
                result["current_item"] = snapshot_graph(item_graph)
            except ColorHostError:
                pass
    return result
