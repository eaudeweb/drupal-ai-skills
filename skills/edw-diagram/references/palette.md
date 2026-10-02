# Palette and accessibility

Each role has four values: the accent (card border and left bar), the tint (card background), the text colour for the technology line, and the legend label. Titles use `#0F172A` and descriptions `#1E293B` on every tint.

| Role | Accent | Tint | Text | Used for |
|---|---|---|---|---|
| `edge` | `#0284C7` | `#E0F2FE` | `#0C4A6E` | Reverse proxy, CDN, load balancer, HTTP cache |
| `app` | `#4F46E5` | `#E0E7FF` | `#312E81` | Web server, CMS, application, API |
| `svc` | `#0D9488` | `#CBFAF6` | `#134E4A` | Redis, Solr, queues, workers, supporting containers |
| `data` | `#C2410C` | `#FFEDD5` | `#7C2D12` | Databases |
| `ext` | `#7C3AED` | `#EDE9FE` | `#4C1D95` | Third-party services, SaaS, analytics, reporting |
| `node` | `#64748B` | `#F1F5F9` | `#1E293B` | Backup storage, file storage, anything else |

Other colours: connectors `#64748B`, connector labels `#334155`, protocol text `#64748B` (on white only), panels `#F4F6F9` with border `#CBD3DD`, boundaries `#94A3B8` dashed, person card `#1E293B`, backup flows use the `data` accent.

## Contrast (WCAG 2)

Measured against the tint of each role:

| Role | Title | Description | Technology | Border and bar |
|---|---|---|---|---|
| `edge` | 15.6 | 12.7 | 8.2 | 3.6 |
| `app` | 14.5 | 11.9 | 9.3 | 5.1 |
| `svc` | 15.8 | 12.9 | 8.4 | 3.3 |
| `data` | 15.6 | 12.8 | 8.2 | 4.5 |
| `ext` | 15.0 | 12.3 | 9.2 | 4.8 |
| `node` | 16.3 | 13.4 | 13.4 | 4.3 |

Requirements: text at least 4.5:1 (AA; the palette reaches 7:1, AAA), borders and bars at least 3:1 (non-text contrast, 1.4.11).

## Adding a role

Use one hue family (Tailwind-style scales work well):

- accent: shade 600-700, at least 3:1 against the tint;
- tint: shade 50-100, light enough for 4.5:1 with `#1E293B`;
- text: shade 900 of the same hue.

```python
d.add_role("queue", "#B45309", "#FEF3C7", "#78350F", "Message queue")
```

`save()` reports any pair below the threshold. To check colours by hand:

```python
from edw_diagram import contrast
contrast("#0D9488", "#CBFAF6")  # 3.31
```

Keep the number of roles per diagram low (five or six). Colour only helps if each colour means one thing.
