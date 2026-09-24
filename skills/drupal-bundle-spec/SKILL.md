---
name: drupal-bundle-spec
description: Write a Drupal bundle specification in the Eau de Web standard format (settings, field table, edit form). Covers content types, taxonomy vocabularies, paragraph types, custom block types and media types. Use when defining, documenting or reviewing any of these or their fields, e.g. "define a content type for events", "define a vocabulary for topics", "document the fields of the accordion paragraph".
---

# Drupal bundle specification

Use this format for every bundle. Keep it factual and short. If the requirements do not say something (e.g. whether the site is multilingual), ask or mark the value as an assumption.

## 1. Settings

The settings depend on the entity type. Use the template for the bundle being specified:

| Entity type | Template |
|---|---|
| Content type (node) | [references/node.md](references/node.md) |
| Taxonomy vocabulary | [references/taxonomy.md](references/taxonomy.md) |
| Paragraph type | [references/paragraph.md](references/paragraph.md) |
| Custom block type | [references/block.md](references/block.md) |
| Media type | [references/media.md](references/media.md) |

Do not copy settings from one entity type to another. For other entity types, list only the settings that exist on their bundle configuration form.

## 2. Field table

| Field label | Field name | Field type | Cardinality | Required | Translatable | Widget | Notes |
|-------------|------------|------------|-------------|----------|--------------|--------|-------|

Column rules:

- **Field label** - name of the field as shown in the edit form.
- **Field name** - machine name with underscores. Use singular for single-value fields (`field_country`) and plural for multi-value fields (`field_countries`).
- **Field type** - Drupal field type, e.g. Entity reference, Entity reference revisions, Text (formatted, long), Date, Link, Media.
- **Cardinality** - 1, 2, ..., or Unlimited. Must match the singular/plural rule of the field name.
- **Required** - Yes/No. Field is required, cannot be left empty.
- **Translatable** - Yes/No. Drop this column when the bundle itself is not translatable.
- **Widget** - input widget shown to the content manager, e.g. Text input, WYSIWYG editor, Autocomplete, Select list, Pop-up view (Entity Browser), Media library, Paragraphs.
- **Notes** - details for developers: target bundles of references, allowed values, vocabulary name, validation, default values, display remarks.

## 3. Edit form

In this section add refinements to the edit form. Name each module the first time it is needed or describe custom code / styles. Use groups, details and tabs to keep the form easy to use.
Here are some examples:

- The scheduled publish date is shown in the Details Sidebar group (using `details_sidebar` from `field_group` and `scheduler` modules).
- The promote and sticky fields are hidden because they are not used.
- The two date fields "Start date" and "End date" are shown next to each other using two-column layout in the administration theme.

Paragraphs have no edit form of their own. Describe their form behaviour on the parent field instead (see [references/paragraph.md](references/paragraph.md)).

## Conventions

- Reuse existing field storage across bundles of the same entity type where the meaning is the same (e.g. one `field_countries` shared by several content types). Field storage cannot be shared between entity types, e.g. a node and a paragraph.
- Entity reference fields state the target entity type and bundles in Notes (e.g. "Taxonomy term: `countries`").
- Base fields are listed in the table when they are used, with their real field names: `title` and `body` for nodes, `name` and `description` for taxonomy terms, `info` for custom blocks, `name` for media.
