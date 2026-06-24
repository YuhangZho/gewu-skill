#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
render_viz.py — structured visual model renderer.

Agent writes only ``<category>/_viz/<concept>.model.json``.
This script validates it, generates Mermaid, and optionally renders SVG with mmdc.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
from pathlib import Path


CHART_TYPES = {"relation", "flow", "hierarchy", "cycle", "state", "sequence"}
KIND_ICONS = {
    "concept": "◉",
    "data": "▣",
    "process": "⚙",
    "actor": "☻",
    "rule": "◆",
    "boundary": "⛔",
    "state": "◇",
    "feedback": "↺",
}
ID_RE = re.compile(r"^[a-z0-9_]+$")


def _err(msg):
    raise ValueError(msg)


def _load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        _err("invalid JSON: %s" % exc)


def _clean_label(label, field="label", max_len=20):
    label = str(label or "").strip()
    if not label:
        _err("%s cannot be empty" % field)
    if max_len and len(label) > max_len:
        _err("%s too long: %s" % (field, label))
    return label


def _validate_id(raw, field="id"):
    value = str(raw or "").strip()
    if not ID_RE.match(value):
        _err("%s must match [a-z0-9_]: %s" % (field, value))
    return value


def _mmd_text(value):
    return str(value or "").replace('"', "'").replace("\n", " ").strip()


def _edge_label(edge):
    label = _mmd_text(edge.get("label", ""))
    return "|%s|" % label if label else ""


def _node_label(node):
    kind = str(node.get("kind") or "concept").strip()
    if kind not in KIND_ICONS:
        _err("kind must be one of %s: %s" % (", ".join(sorted(KIND_ICONS)), kind))
    return "%s %s" % (KIND_ICONS[kind], _clean_label(node.get("label")))


def _validate_nodes(data, minimum=2):
    raw_nodes = data.get("nodes")
    if not isinstance(raw_nodes, list) or len(raw_nodes) < minimum:
        _err("nodes must contain at least %d items" % minimum)
    if len(raw_nodes) > 12:
        _err("nodes cannot exceed 12")
    seen = set()
    nodes = []
    for raw in raw_nodes:
        if not isinstance(raw, dict):
            _err("node must be an object")
        node_id = _validate_id(raw.get("id"))
        if node_id in seen:
            _err("duplicate node id: %s" % node_id)
        seen.add(node_id)
        node = dict(raw)
        node["id"] = node_id
        node["label"] = _clean_label(node.get("label"))
        node["kind"] = str(node.get("kind") or "concept").strip()
        if node["kind"] not in KIND_ICONS:
            _err("kind must be one of %s: %s" % (", ".join(sorted(KIND_ICONS)), node["kind"]))
        nodes.append(node)
    return nodes


def _validate_edges(data, node_ids, minimum=1):
    raw_edges = data.get("edges")
    if not isinstance(raw_edges, list) or len(raw_edges) < minimum:
        _err("edges must contain at least %d items" % minimum)
    edges = []
    for raw in raw_edges:
        if not isinstance(raw, dict):
            _err("edge must be an object")
        src = _validate_id(raw.get("from"), "edge.from")
        dst = _validate_id(raw.get("to"), "edge.to")
        if src not in node_ids:
            _err("edge.from unknown node: %s" % src)
        if dst not in node_ids:
            _err("edge.to unknown node: %s" % dst)
        style = str(raw.get("style") or "solid").strip()
        if style not in ("solid", "dashed"):
            _err("edge.style must be solid or dashed")
        edge = dict(raw)
        edge["from"] = src
        edge["to"] = dst
        edge["style"] = style
        edges.append(edge)
    return edges


def _validate_common(data):
    if not isinstance(data, dict):
        _err("model must be an object")
    if "secondary_chart" in data:
        _err("secondary_chart is not allowed; use exactly one main chart")
    if "charts" in data:
        _err("charts is not allowed; use exactly one main chart")
    chart_type = str(data.get("chart_type") or "").strip()
    if chart_type not in CHART_TYPES:
        _err("chart_type must be one of %s" % ", ".join(sorted(CHART_TYPES)))
    concept = _clean_label(data.get("concept"), "concept", max_len=80)
    return chart_type, concept


def validate_model(data):
    chart_type, concept = _validate_common(data)
    model = dict(data)
    model["chart_type"] = chart_type
    model["concept"] = concept
    if chart_type in ("relation", "flow", "hierarchy", "cycle"):
        nodes = _validate_nodes(model, 3 if chart_type == "cycle" else 2)
        edges = _validate_edges(model, {n["id"] for n in nodes}, 1)
        model["nodes"] = nodes
        model["edges"] = edges
    elif chart_type == "state":
        states = model.get("states")
        transitions = model.get("transitions")
        if not isinstance(states, list) or len(states) < 2:
            _err("states must contain at least 2 items")
        if len(states) > 12:
            _err("states cannot exceed 12")
        out_states = []
        seen = set()
        for raw in states:
            if not isinstance(raw, dict):
                _err("state must be an object")
            sid = _validate_id(raw.get("id"), "state.id")
            if sid in seen:
                _err("duplicate state id: %s" % sid)
            seen.add(sid)
            out_states.append({"id": sid, "label": _clean_label(raw.get("label"), "state.label")})
        if not isinstance(transitions, list) or not transitions:
            _err("transitions must contain at least 1 item")
        out_transitions = []
        for raw in transitions:
            src = _validate_id(raw.get("from"), "transition.from")
            dst = _validate_id(raw.get("to"), "transition.to")
            if src not in seen or dst not in seen:
                _err("transition references unknown state")
            out_transitions.append(dict(raw, **{"from": src, "to": dst}))
        model["states"] = out_states
        model["transitions"] = out_transitions
    elif chart_type == "sequence":
        actors = model.get("actors")
        messages = model.get("messages")
        if not isinstance(actors, list) or len(actors) < 2:
            _err("actors must contain at least 2 items")
        seen = set()
        out_actors = []
        for raw in actors:
            if not isinstance(raw, dict):
                _err("actor must be an object")
            aid = _validate_id(raw.get("id"), "actor.id")
            if aid in seen:
                _err("duplicate actor id: %s" % aid)
            seen.add(aid)
            out_actors.append({"id": aid, "label": _clean_label(raw.get("label"), "actor.label")})
        if not isinstance(messages, list) or not messages:
            _err("messages must contain at least 1 item")
        out_messages = []
        for raw in messages:
            src = _validate_id(raw.get("from"), "message.from")
            dst = _validate_id(raw.get("to"), "message.to")
            if src not in seen or dst not in seen:
                _err("message references unknown actor")
            label = _clean_label(raw.get("label"), "message.label")
            out_messages.append(dict(raw, **{"from": src, "to": dst, "label": label}))
        model["actors"] = out_actors
        model["messages"] = out_messages
    return model


def _render_node_defs(nodes):
    return ["  %s[\"%s\"]" % (n["id"], _mmd_text(_node_label(n))) for n in nodes]


def _render_edges(edges):
    out = []
    for edge in edges:
        arrow = "-.->" if edge.get("style") == "dashed" else "-->"
        out.append("  %s %s%s %s" % (edge["from"], arrow, _edge_label(edge), edge["to"]))
    return out


def render_relation(model):
    return "\n".join(["graph LR"] + _render_node_defs(model["nodes"]) + _render_edges(model["edges"])) + "\n"


def render_flow(model):
    return "\n".join(["flowchart TD"] + _render_node_defs(model["nodes"]) + _render_edges(model["edges"])) + "\n"


def render_hierarchy(model):
    return "\n".join(["flowchart TD"] + _render_node_defs(model["nodes"]) + _render_edges(model["edges"])) + "\n"


def render_cycle(model):
    return "\n".join(["flowchart LR"] + _render_node_defs(model["nodes"]) + _render_edges(model["edges"])) + "\n"


def render_state(model):
    lines = ["stateDiagram-v2"]
    for state in model["states"]:
        lines.append('  state "%s" as %s' % (_mmd_text("◇ " + state["label"]), state["id"]))
    for tran in model["transitions"]:
        trigger = _mmd_text(tran.get("trigger") or tran.get("label") or "")
        suffix = " : %s" % trigger if trigger else ""
        lines.append("  %s --> %s%s" % (tran["from"], tran["to"], suffix))
    return "\n".join(lines) + "\n"


def render_sequence(model):
    lines = ["sequenceDiagram"]
    for actor in model["actors"]:
        lines.append("  participant %s as %s" % (actor["id"], _mmd_text("☻ " + actor["label"])))
    for msg in model["messages"]:
        lines.append("  %s->>%s: %s" % (msg["from"], msg["to"], _mmd_text(msg["label"])))
        note = _mmd_text(msg.get("note") or "")
        if note:
            lines.append("  Note over %s,%s: %s" % (msg["from"], msg["to"], note))
    return "\n".join(lines) + "\n"


RENDERERS = {
    "relation": render_relation,
    "flow": render_flow,
    "hierarchy": render_hierarchy,
    "cycle": render_cycle,
    "state": render_state,
    "sequence": render_sequence,
}


def render_mermaid(data):
    model = validate_model(data)
    return RENDERERS[model["chart_type"]](model), model


def _run_mmdc(mmd_path, svg_path):
    exe = shutil.which("mmdc")
    if not exe:
        return False
    subprocess.run([exe, "-i", str(mmd_path), "-o", str(svg_path)], check=True)
    return True


def render_model(vault, cat, concept, make_svg=True):
    vault = Path(vault)
    viz_dir = vault / cat / "_viz"
    model_path = viz_dir / ("%s.model.json" % concept)
    data = _load_json(model_path)
    mmd, model = render_mermaid(data)
    viz_dir.mkdir(parents=True, exist_ok=True)
    mmd_path = viz_dir / ("%s.mmd" % concept)
    svg_path = viz_dir / ("%s.svg" % concept)
    mmd_path.write_text(mmd, encoding="utf-8")
    svg_written = False
    if make_svg:
        svg_written = _run_mmdc(mmd_path, svg_path)
    return {
        "model": str(model_path),
        "mmd": str(mmd_path),
        "svg": str(svg_path) if svg_written else "",
        "chart_type": model["chart_type"],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", required=True)
    ap.add_argument("--cat", required=True)
    ap.add_argument("--concept", required=True)
    ap.add_argument("--no-svg", action="store_true")
    args = ap.parse_args()
    result = render_model(args.vault, args.cat, args.concept, make_svg=not args.no_svg)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
