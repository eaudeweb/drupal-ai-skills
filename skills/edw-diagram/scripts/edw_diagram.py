#!/usr/bin/env python3
"""Small library for hand-laid-out SVG architecture diagrams in the Eau de Web style.

Every element is placed with explicit coordinates. The library takes care of the
look (palette, cards, connectors, labels, legend), the drawing order and a few
automatic checks (WCAG contrast, text overflow, overlapping cards).

Example:

    from edw_diagram import Diagram

    d = Diagram(900, 500, "Infrastructure Diagram - Example", "Hosting and data flows")
    d.panel(40, 120, 380, 300, "Production server")
    d.card(80, 170, 300, 60, "NGINX", "Reverse proxy", role="edge")
    d.card(80, 290, 300, 78, "Drupal", "PHP-FPM", "Generate dynamic pages", role="app")
    d.arrow([(230, 230), (230, 286)], "FastCGI", "Unix socket", at=(240, 255), anchor="start")
    d.legend(440, 380)
    d.save("diagram.svg")
"""
from __future__ import annotations

import sys
from html import escape

FONT = "'Noto Sans', 'Helvetica Neue', Arial, sans-serif"
MONO = "'DejaVu Sans Mono', 'Menlo', monospace"

INK = "#0F172A"      # titles
DESC = "#1E293B"     # descriptions inside cards
SUB = "#475569"      # secondary text on white or grey
MUTED = "#64748B"    # captions on white only (4.76:1)
LINE = "#64748B"     # connectors
LABEL = "#334155"    # connector labels
BORDER = "#D5DCE5"   # legend frame
PANEL_BG = "#F4F6F9"
PANEL_BORDER = "#CBD3DD"
BOUNDARY = "#94A3B8"

# role: (accent - bar and border, tint - background, text - technology line, legend label)
ROLES = {
    "edge": ("#0284C7", "#E0F2FE", "#0C4A6E", "Proxy and HTTP cache"),
    "app": ("#4F46E5", "#E0E7FF", "#312E81", "Web and application"),
    "svc": ("#0D9488", "#CBFAF6", "#134E4A", "Supporting services"),
    "data": ("#C2410C", "#FFEDD5", "#7C2D12", "Database"),
    "ext": ("#7C3AED", "#EDE9FE", "#4C1D95", "Third-party service"),
    "node": ("#64748B", "#F1F5F9", "#1E293B", "Storage and other"),
}

# kind: (colour, dashed, arrow head, legend label)
FLOWS = {
    "request": (LINE, False, True, "Request"),
    "backup": ("#C2410C", True, True, "Backup"),
    "integration": (LINE, True, False, "Integration"),
}


# ---------------------------------------------------------------------------
# WCAG helpers
# ---------------------------------------------------------------------------
def luminance(hex_colour: str) -> float:
    h = hex_colour.lstrip("#")
    rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    rgb = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]


def contrast(a: str, b: str) -> float:
    la, lb = sorted([luminance(a), luminance(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


def text_width(s: str, size: float, weight: int = 400) -> float:
    """Rough width estimate for Noto Sans, good enough to catch overflow."""
    factor = 0.58 if weight >= 600 else 0.52
    return len(s) * size * factor


# ---------------------------------------------------------------------------
# Diagram
# ---------------------------------------------------------------------------
class Diagram:
    def __init__(self, width: int, height: int, title: str = "", subtitle: str = ""):
        self.w, self.h = width, height
        self.title, self.subtitle = title, subtitle
        self.roles = dict(ROLES)
        self.flows = dict(FLOWS)
        # Drawing order: groups, connectors, nodes, labels on top.
        self.layers: dict[str, list[str]] = {"groups": [], "lines": [], "nodes": [], "labels": []}
        self.defs: list[str] = []
        self.boxes: list[tuple[str, float, float, float, float]] = []
        self.warnings: list[str] = []
        self._ids = 0
        self.used_roles: list[str] = []
        self.used_flows: list[str] = []

    # -- configuration ------------------------------------------------------
    def add_role(self, key: str, accent: str, tint: str, text: str, legend: str):
        """Add or override a role. Contrast is checked on save."""
        self.roles[key] = (accent, tint, text, legend)

    # -- low level ----------------------------------------------------------
    def _id(self, prefix: str) -> str:
        self._ids += 1
        return f"{prefix}{self._ids}"

    def text(self, x, y, s, size=12, weight=400, fill=INK, anchor="start", family=FONT,
             halo=False, layer="labels"):
        extra = ""
        if halo:
            extra = ' stroke="#FFFFFF" stroke-width="4" stroke-linejoin="round" paint-order="stroke"'
        self.layers[layer].append(
            f'<text x="{x:g}" y="{y:g}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{extra}>{escape(s)}</text>'
        )

    def _track(self, kind, x, y, w, h):
        self.boxes.append((kind, x, y, w, h))

    def _use_role(self, role):
        if role not in self.roles:
            raise KeyError(f"Unknown role '{role}'. Known roles: {', '.join(self.roles)}")
        if role not in self.used_roles:
            self.used_roles.append(role)
        return self.roles[role]

    # -- grouping -----------------------------------------------------------
    def boundary(self, x, y, w, h, lines, caption=""):
        """Dashed frame for an organisation or provider (e.g. hosting company, cloud)."""
        self.layers["groups"].append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="none" '
            f'stroke="{BOUNDARY}" stroke-width="1.5" stroke-dasharray="7 5"/>'
        )
        lines = [lines] if isinstance(lines, str) else lines
        yy = y + 26
        for i, s in enumerate(lines):
            self.text(x + 20, yy, s, 14 if i == 0 else 13, 700 if i == 0 else 600, INK, layer="groups")
            yy += 18
        if caption:
            self.text(x + 20, yy, caption, 11, 400, MUTED, layer="groups")

    def panel(self, x, y, w, h, title, sub=None):
        """Grey panel for a server, environment or managed service."""
        self.layers["groups"].append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{PANEL_BG}" stroke="{PANEL_BORDER}"/>'
        )
        self.text(x + 18, y + 26, title, 13, 700, INK, layer="groups")
        if sub:
            self.text(x + 18, y + 43, sub, 11, 400, SUB, layer="groups")

    # -- nodes --------------------------------------------------------------
    def card(self, x, y, w, h, title, tech=None, desc=None, role="app"):
        """Card with tinted background, accent border and accent bar on the left.

        Heights: 52-60 for one or two lines, 72-78 for three lines.
        """
        accent, tint, txt, _ = self._use_role(role)
        cid = self._id("clip")
        n = self.layers["nodes"]
        n.append(f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/></clipPath>')
        n.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{tint}" stroke="{accent}" '
            f'stroke-width="1.25" filter="url(#shadow)"/>'
        )
        n.append(f'<rect x="{x}" y="{y}" width="6" height="{h}" fill="{accent}" clip-path="url(#{cid})"/>')
        cx = x + w / 2 + 3
        lines = 1 + (tech is not None) + (desc is not None)
        yy = y + h / 2 - (lines - 1) * 9 + 5
        self.text(cx, yy, title, 14, 700, INK, "middle", layer="nodes")
        if tech:
            yy += 18
            self.text(cx, yy, tech, 11, 600, txt, "middle", layer="nodes")
        if desc:
            yy += 18
            self.text(cx, yy, desc, 12, 400, DESC, "middle", layer="nodes")
        self._check_fit(title, w, 14, 700)
        if tech:
            self._check_fit(tech, w, 11, 600)
        if desc:
            self._check_fit(desc, w, 12, 400)
        needed = 22 + lines * 18
        if h < needed - 4:
            self.warnings.append(f"Card '{title}' is {h}px high, {needed}px recommended for {lines} line(s)")
        self._track(f"card '{title}'", x, y, w, h)

    def database(self, cx, cy, w, h, title, tech=None, role="data"):
        """Cylinder for a database, centred on (cx, cy)."""
        accent, tint, txt, _ = self._use_role(role)
        x, ry = cx - w / 2, 9
        top, bot = cy - h / 2, cy + h / 2
        n = self.layers["nodes"]
        n.append(
            f'<path d="M{x},{top + ry} A{w / 2},{ry} 0 0 1 {x + w},{top + ry} V{bot - ry} '
            f'A{w / 2},{ry} 0 0 1 {x},{bot - ry} Z" fill="{tint}" stroke="{accent}" stroke-width="1.25" '
            f'filter="url(#shadow)"/>'
        )
        n.append(
            f'<ellipse cx="{cx}" cy="{top + ry}" rx="{w / 2}" ry="{ry}" fill="{tint}" '
            f'stroke="{accent}" stroke-width="1.25"/>'
        )
        self.text(cx, cy + 8, title, 14, 700, INK, "middle", layer="nodes")
        if tech:
            self.text(cx, cy + 26, tech, 11, 600, txt, "middle", layer="nodes")
        self._check_fit(title, w, 14, 700)
        self._track(f"database '{title}'", x, top, w, h)

    def person(self, cx, y, label, w=170, h=84):
        """Dark card with a person icon for users, visitors or editors."""
        x = cx - w / 2
        n = self.layers["nodes"]
        n.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#1E293B" filter="url(#shadow)"/>')
        n.append(f'<circle cx="{cx}" cy="{y + 24}" r="10" fill="#E2E8F0"/>')
        n.append(
            f'<path d="M{cx - 17},{y + 52} Q{cx - 17},{y + 36} {cx},{y + 36} '
            f'Q{cx + 17},{y + 36} {cx + 17},{y + 52} Z" fill="#E2E8F0"/>'
        )
        self.text(cx, y + 72, label, 13, 700, "#FFFFFF", "middle", layer="nodes")
        self._check_fit(label, w, 13, 700)
        self._track(f"person '{label}'", x, y, w, h)

    # -- connectors ---------------------------------------------------------
    def arrow(self, points, label=None, proto=None, at=None, anchor="middle", kind="request", head=None):
        """Orthogonal connector through a list of (x, y) points.

        label/proto are drawn at `at` (x, y of the first line). Use anchor="start"
        to place the text to the right of a vertical segment, "middle" above a
        horizontal one. kind is one of: request, backup, integration.
        """
        colour, dashed, default_head, _ = self.flows[kind]
        if kind not in self.used_flows:
            self.used_flows.append(kind)
        head = default_head if head is None else head
        for (x1, y1), (x2, y2) in zip(points, points[1:]):
            if x1 != x2 and y1 != y2:
                self.warnings.append(f"Diagonal segment {x1},{y1} -> {x2},{y2}; keep connectors orthogonal")
        d = "M" + " L".join(f"{x:g},{y:g}" for x, y in points)
        dash = ' stroke-dasharray="6 5"' if dashed else ""
        marker = f' marker-end="url(#{self._marker(colour)})"' if head else ""
        self.layers["lines"].append(
            f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="1.6" stroke-linejoin="round"{dash}{marker}/>'
        )
        if label or proto:
            if at is None:
                raise ValueError(f"Label '{label}' needs at=(x, y)")
            lx, ly = at
            text_colour = self.roles["data"][2] if kind == "backup" else LABEL
            if label:
                self.text(lx, ly, label, 11, 600, text_colour, anchor, halo=True)
            if proto:
                self.text(lx, ly + (15 if label else 0), proto, 10.5, 400, MUTED, anchor, MONO, halo=True)

    def _marker(self, colour):
        mid = "arrow" + colour.lstrip("#")
        if not any(f'id="{mid}"' in s for s in self.defs):
            self.defs.append(
                f'<marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" '
                f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{colour}"/></marker>'
            )
        return mid

    # -- legend -------------------------------------------------------------
    def legend(self, x, y, roles=None, flows=None, col_width=152):
        """Legend with the roles and flow kinds used (or the lists given)."""
        roles = roles or [k for k in self.roles if k in self.used_roles]
        flows = flows or [k for k in self.flows if k in self.used_flows]
        rows = max((len(roles) + 1) // 2, len(flows))
        w = 16 + 2 * col_width + 110
        h = 40 + rows * 20 + 4
        g = self.layers["labels"]
        g.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#FFFFFF" stroke="{BORDER}"/>')
        self.text(x + 16, y + 22, "Legend", 12, 700, INK)
        for i, key in enumerate(roles):
            accent, tint, _, label = self.roles[key]
            cx = x + 16 + (i % 2) * col_width
            cy = y + 40 + (i // 2) * 20
            g.append(f'<rect x="{cx}" y="{cy}" width="12" height="13" rx="2" fill="{tint}" stroke="{accent}"/>')
            g.append(f'<rect x="{cx}" y="{cy}" width="3" height="13" fill="{accent}"/>')
            self.text(cx + 18, cy + 11, label, 11, 400, SUB)
        sx = x + 16 + 2 * col_width
        for i, kind in enumerate(flows):
            colour, dashed, head, label = self.flows[kind]
            yy = y + 46 + i * 20
            dash = ' stroke-dasharray="6 5"' if dashed else ""
            marker = f' marker-end="url(#{self._marker(colour)})"' if head else ""
            g.append(f'<path d="M{sx},{yy} H{sx + 30}" stroke="{colour}" stroke-width="1.6"{dash}{marker}/>')
            self.text(sx + 38, yy + 4, label, 11, 400, SUB)
        self._track("legend", x, y, w, h)

    # -- checks -------------------------------------------------------------
    def _check_fit(self, s, w, size, weight):
        if text_width(s, size, weight) > w - 16:
            self.warnings.append(f"Text '{s}' may not fit in {w}px; widen the box or shorten the text")

    def check(self):
        """Return warnings: contrast below WCAG AA, overflow, overlaps, out of canvas."""
        out = list(self.warnings)
        for key in self.used_roles:
            accent, tint, txt, _ = self.roles[key]
            for name, fg, need in (("title", INK, 4.5), ("description", DESC, 4.5),
                                   ("technology", txt, 4.5), ("border/bar", accent, 3.0)):
                r = contrast(fg, tint)
                if r < need:
                    out.append(f"Role '{key}': {name} {fg} on {tint} is {r:.2f}:1, needs {need}:1")
        cards = [b for b in self.boxes]
        for i, (a, ax, ay, aw, ah) in enumerate(cards):
            if ax < 10 or ay < 10 or ax + aw > self.w - 10 or ay + ah > self.h - 10:
                out.append(f"{a} is outside the canvas ({self.w}x{self.h}) or closer than 10px to the edge")
            for b, bx, by, bw, bh in cards[i + 1:]:
                if ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah:
                    out.append(f"{a} overlaps {b}")
        return out

    # -- output -------------------------------------------------------------
    def svg(self) -> str:
        head = []
        if self.title:
            head.append(
                f'<text x="40" y="52" font-family="{FONT}" font-size="24" font-weight="700" '
                f'fill="{INK}">{escape(self.title)}</text>'
            )
        if self.subtitle:
            head.append(
                f'<text x="40" y="76" font-family="{FONT}" font-size="13" fill="{MUTED}">{escape(self.subtitle)}</text>'
            )
        body = "\n".join(head + self.layers["groups"] + self.layers["lines"] + self.layers["nodes"] + self.layers["labels"])
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}">
<title>{escape(self.title)}</title>
<defs>
  {"  ".join(self.defs)}
  <filter id="shadow" x="-10%" y="-10%" width="120%" height="140%">
    <feDropShadow dx="0" dy="1.5" stdDeviation="2" flood-color="#0F172A" flood-opacity="0.10"/>
  </filter>
</defs>
<rect width="{self.w}" height="{self.h}" fill="#FFFFFF"/>
{body}
</svg>
'''

    def save(self, path: str, strict: bool = False):
        """Write the SVG and print any warnings to stderr."""
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.svg())
        problems = self.check()
        for p in problems:
            print(f"WARNING: {p}", file=sys.stderr)
        print(f"Saved {path} ({len(problems)} warning(s))", file=sys.stderr)
        if strict and problems:
            sys.exit(1)
        return problems
