---
name: edw-diagram
description: Draw architecture, infrastructure, deployment and integration diagrams as hand-laid-out SVG and PNG in the Eau de Web visual style (tinted cards with a coloured bar, WCAG AA palette, orthogonal connectors, legend). Use whenever a diagram or schematic is needed for a proposal, tender, technical documentation or README - for example "draw the hosting architecture", "make a nicer version of this PlantUML / Mermaid diagram", "diagram how Drupal talks to Solr, Redis and the database", "infrastructure schema for the offer" - even if the user does not name a format or mentions PlantUML, C4 or draw.io.
---

# Eau de Web diagrams

Diagrams are drawn with explicit coordinates through a small Python library, not with an auto-layout tool. Auto-layout (PlantUML, Graphviz, Mermaid) places columns and labels unpredictably; a manual layout gives symmetric columns, connectors that do not cross and labels that stay next to their line. The library handles the look and runs automatic checks, so the work is mostly planning the layout.

Bundled files:

- `scripts/edw_diagram.py` - the library (`Diagram` with `boundary`, `panel`, `card`, `database`, `person`, `arrow`, `legend`, `save`).
- `scripts/render.py` - SVG to PNG with headless Chrome or `rsvg-convert`.
- `assets/example_infrastructure.py` - complete worked example (two Drupal stacks, shared database, backups, external services). Read it before writing a new diagram; copying its structure is the fastest route. `assets/example.svg` is its output and shows the target look.
- `references/layout.md` - layout rules and connector routing. Read it when planning.
- `references/palette.md` - roles, colours and contrast values. Read it when adding a role or changing colours.

## Workflow

1. **Collect the model.** List the nodes (with name, technology, short description), the groups (organisation or provider, server or environment) and the connections (label, protocol or port). If the input is an existing diagram (PlantUML, Mermaid, sketch), keep its content exactly - same names, labels and connections - unless the user asks for changes. Point out errors you notice instead of silently fixing them.
2. **Assign roles.** Each node gets one role: `edge` (proxy, CDN, HTTP cache), `app` (web server, CMS, application), `svc` (Redis, Solr, queues, supporting containers), `data` (databases), `ext` (third-party and SaaS), `node` (backup storage, file storage, anything else). Each connector gets a kind: `request`, `backup` or `integration` (undirected, dashed).
3. **Plan the layout on paper first.** Decide columns and rows before writing code (see `references/layout.md`). Write the plan as a comment at the top of the script, as in the example.
4. **Write the generator** next to the output, e.g. `<name>.py`, importing the library from the skill directory:
   ```python
   sys.path.insert(0, "<skill-dir>/scripts")
   from edw_diagram import Diagram
   ```
   For a project that keeps diagrams in version control, copy `edw_diagram.py` next to the generator so the diagram still builds without the skill.
5. **Generate and render:**
   ```bash
   python3 <name>.py <name>.svg
   python3 <skill-dir>/scripts/render.py <name>.svg <name>.png --scale 1
   ```
   Fix every warning printed by `save()` (contrast, text overflow, overlapping boxes, diagonal segments, content outside the canvas).
6. **Look at the PNG.** Open the image and check what the automatic checks cannot see: crossing connectors, labels touching lines or boxes, arrows ending inside a box instead of at its edge, uneven gaps, empty areas. Adjust coordinates and render again. Expect two or three rounds.
7. **Deliver** the generator script, the SVG and a PNG at `--scale 2` (for Word and PDF). Name the files after the diagram, not after the tool.

## Style rules in short

- One look for all diagrams: white canvas, title top left with an optional grey subtitle, groups as grey panels or dashed boundaries, nodes as tinted cards with an accent bar and border, legend bottom right.
- Text inside cards: bold title, technology in the role's dark text colour, description in dark slate. Keep each line short; widen the card rather than wrapping.
- Do not invent new colours per diagram. If a new role is needed, add it with `d.add_role()` using the method in `references/palette.md`; `save()` checks its contrast.
- Labels belong to the connector: to the right of a vertical segment (`anchor="start"`) or centred above a horizontal one.
- British English, sentence-case labels in new diagrams, no em dashes.
