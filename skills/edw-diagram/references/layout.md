# Layout and connector routing

## Planning

1. **Find the main flow.** Usually a request travels from a person to an edge component, through the application to data. Draw it top to bottom inside a column.
2. **Use columns for parallel things.** Environments (production, staging), sites or tenants that share a structure go side by side as mirrored columns. Production is always the leftmost column.
3. **Put shared resources between the columns they serve.** A database used by two stacks goes in a central column, so both connectors are short horizontal lines and do not cross.
4. **Put people and external services at the top**, centred on the axis of the diagram, outside the hosting boundary. Put things that sit outside the hosting provider (off-site backup, SaaS) outside the boundary as well.
5. **Side column for loosely connected services** (analytics, monitoring) on the right, inside or outside the boundary as appropriate.
6. **Write the plan as a comment** with x ranges per column and y ranges per band (header, actors, boundary, outside). It keeps later edits consistent.

## Grid and sizes (starting values)

| Item | Value |
|---|---|
| Canvas width | 1200-1700 px; height to fit, at least 10 px margin |
| Title / subtitle baseline | y = 52 / 76, x = 40 |
| Boundary | rx 16, label block 50-70 px high at the top left |
| Panel padding | 20-30 px around cards, 55 px from panel top to first card |
| Card width | 160-300 px; one card column per panel is easiest to read |
| Card height | 52-60 px (1-2 lines), 72-78 px (3 lines) |
| Vertical gap between cards | 40 px without a label, 76-80 px with a two-line label |
| Gap between columns | at least 110 px if a labelled connector crosses it |
| Person card | 170 x 84 px |
| Database cylinder | 150 x 82 px |

Align card centres on shared axes. Mirrored columns use the same y values, so the eye can compare them.

## Connectors

- **Orthogonal only.** Each connector is a list of points with horizontal and vertical segments. The library warns about diagonal segments.
- **End at the edge of the target.** The arrow tip sits at the end point, so stop 3-4 px before the border (e.g. target top at y = 475, end at y = 471).
- **Leave a person or hub sideways**, then drop vertically into the target. Different targets leave at different y values (e.g. 112, 130, 148) so the lines do not overlap.
- **No crossings.** If two connectors would cross, move a node or route one through free space (between columns, between panels, through the margin of the boundary). A crossing usually means a node is in the wrong column.
- **Several connectors from one node** leave from different points of the same side, at least 20 px apart.
- **Undirected integrations** (`kind="integration"`) have no arrow head and are dashed grey.

## Labels

- First line: what flows (bold, e.g. "SQL queries"); second line: protocol or port in monospace (e.g. "TCP/3306"). Either line may be omitted.
- Vertical segment: `at=(line_x + 8..10, middle_y)`, `anchor="start"`.
- Horizontal segment: `at=(middle_x, line_y - 28)`, `anchor="middle"`; both lines then sit above the line.
- Labels have a white halo, so they can sit over a panel border, but never over another line or a card.
- Keep labels inside the gap they describe. If a label does not fit, widen the gap rather than shrinking the text.

## Final visual check

Render at scale 1 and look for:

- connectors crossing each other or passing through a card;
- labels touching a box, another label or the wrong line;
- uneven spacing between similar elements, or mirrored columns that are not aligned;
- large empty areas (reduce the canvas) or crowded areas (increase gaps);
- the legend overlapping content.
