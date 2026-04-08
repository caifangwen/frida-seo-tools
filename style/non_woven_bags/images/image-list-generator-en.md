## Task

Analyze the article content, list all required images, and provide for each image:

1. Image purpose description
2. Detailed Alt text (8-15 words, including keywords)
3. Descriptive filename (lowercase + hyphens, 5-8 keywords)

## Image Density Rules

- At least 1 image per 400-500 words
- At least 1 image per H2 section
- First section after introduction must have an image
- One image before and after comparison tables
- One summary image before conclusion (optional)

## Filename Naming Rules

- All lowercase letters
- Connect words with hyphens `-`
- Avoid special characters and spaces
- Keep descriptive but concise (5-8 keywords)
- Length not exceeding 60 characters

## Alt Text Rules

- Length 8-15 words
- Describe the specific content of the image
- Include target keywords
- Avoid starting with "image of" or "picture of"
- Use specific scenarios and detailed descriptions

## Output

- Article-name-images-list.json

- Encoding: UTF-8

- Output format (JSON):

```json
{
  "article": "article-name",
  "images": [
    {
      "no": 1,
      "position": "After/Before which section",
      "purpose": "Describe image purpose",
      "alt_text": "Detailed alt description",
      "filename": "topic-description-detail.webp",
      "upload_path": "/wp-content/uploads/YYYYMMDD/filename.webp",
      "search_keywords": ["keyword1", "keyword2", "keyword3"]
    }
  ]
}
```
