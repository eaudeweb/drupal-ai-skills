# Media type settings

```
* Name: `Document`
* Machine name: `document`
* Description: `PDF and office files attached to content.`
* Media source: Image / File / Remote video / Audio file / Video file / other
* Source field: `field_media_document`
* Allowed file extensions: `pdf docx xlsx`
* Maximum file size: `20 MB`
* Field mapping: Name -> `name`
* Publishing options:
    * Published: Yes/No
    * Create new revision: Yes/No
* Enable translation: Yes/No
* Media pages: Not accessible / Public
```

- **Source field** - list it in the field table as well, with its type (Image, File, Plain text for remote video URLs).
- **Field mapping** - metadata from the source copied into fields, e.g. image width or remote video title. Write "None" when not used.
- **Media pages** - default is Not accessible. Media entities are used inside content, so their own pages (`/media/{id}`) are not public. The standalone URL is a site-wide setting and is off by default; to control it per media type use `rabbit_hole`.
- Media pages only hide the entity page. Files stored in `public://` stay reachable through their direct URL. Files that must be restricted use the private file system - state this in the Notes of the source field.
