## Task

Analyze the article content and image list (JSON), then insert Markdown image links at the specified positions in the article.

## Input Files

1. **Article**: Markdown file (e.g., `welding-procedure-specifications-wps-guide.md`)
2. **Image List**: JSON file (e.g., `welding-procedure-specifications-wps-guide-images-list.json`)

## Insertion Rules

### Position Matching

Match the `position` field from JSON to article sections:

| Position Value | Insertion Point |
|---------------|-----------------|
| `After 'X' section` | Insert after the section content, before next H2 |
| `Before 'X' section` | Insert before the section H2 heading |
| `After [H2 heading]` | Insert after the first paragraph following that H2 |

### Image Link Format

```markdown
![alt_text](./assets/images/folder/filename.webp)
```

**Requirements:**
- Use relative path starting with `./assets/images/`
- Add blank line before and after image link
- Image should be on its own line

### Spacing Rules

- Always add one blank line before the image link
- Always add one blank line after the image link
- Never insert image inside code blocks or tables

## JSON Structure

```json
{
  "article": "article-name",
  "images": [
    {
      "no": 1,
      "position": "After 'What Is a WPS' section",
      "purpose": "Description",
      "alt_text": "Detailed alt text 8-15 words",
      "filename": "image-name.webp",
      "upload_path": "/wp-content/uploads/...",
      "search_keywords": ["keyword1", "keyword2"]
    }
  ]
}
```

## Output

- Modified Markdown file with image links inserted
- Maintain original article structure
- Report which images were inserted and where

## Example

**Before:**
```markdown
## What Is a WPS?

Content paragraph here.

## Why You Need WPS

More content.
```

**After:**
```markdown
## What Is a WPS?

Content paragraph here.

![industrial welding procedure specification document on site](./assets/images/wps-guide/wps-document-industrial-pipeline-site.webp)

## Why You Need WPS

More content.
```

## Workflow

1. Read the article Markdown file
2. Read the image list JSON file
3. For each image in the list:
   - Find the matching section in the article
   - Determine exact insertion point
   - Insert Markdown image link with proper spacing
4. Save the modified article
5. Report insertion results
