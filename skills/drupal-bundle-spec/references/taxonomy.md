# Taxonomy vocabulary settings

```
* Name: `Topics`
* Machine name: `topics`
* Description: `Thematic areas used to classify content.`
* Hierarchy: Flat / Multi-level (max. depth)
* Create new revision: Yes/No
* Enable translation: Yes/No
* Term pages: Public / Not accessible
* Managed by: Content managers / Administrators only / Imported (source)
```

- **Hierarchy** - Drupal does not store this as a vocabulary setting. State it so developers and content managers know the expected structure.
- **Term pages** - when terms are only used for classification, the term page is usually disabled (e.g. `rabbit_hole`) or replaced by a filtered view.
- **Managed by** - who creates and edits the terms. For imported lists (e.g. ISO countries), name the source and how updates are applied.
- Creating new terms from an autocomplete field is set on the referencing field, not on the vocabulary. Mention it in the Notes column of that field.
- Vocabularies with a fixed initial list: attach the list or state where it is located.
