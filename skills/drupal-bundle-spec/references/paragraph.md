# Paragraph type settings

```
* Label: `Accordion`
* Machine name: `accordion`
* Description: `A list of collapsible items with a title and text.`
* Icon: Yes/No
* Used in: `node.web_page.field_components`, `node.event.field_components`
* Enable translation: Yes/No
```

- **Used in** - the parent fields that allow this paragraph type. The allowed types are configured on each parent field (Entity reference revisions), so repeat them in the Notes column of that field.
- **Translation** - the parent paragraph field is not translatable; the fields inside the paragraph are. Use the Translatable column in the field table for those fields.
- Nested paragraphs (a paragraph field inside a paragraph) are listed like any other field. Avoid more than two levels.

## Form behaviour on the parent field

Describe this in the Edit form section of the parent bundle, or in the Notes of the parent field:

- Widget: Paragraphs (stable) or Paragraphs Classic.
- Edit mode: Open / Closed / Closed, show nested.
- Add mode: Dropdown button / Buttons / Modal form.
- Default paragraph type added on a new entity, if any.
