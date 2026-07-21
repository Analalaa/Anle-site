---
title: Example Blog Post Title
title_zh: 示例博客文章标题
description: This is a short description for SEO and social sharing.
description_zh: 这是一段用于 SEO 和社交分享的简短描述。
date: 2026-05-17
category: Work Insights
category_zh: 工作洞察
slug: example-blog-post
image: /images/blog/87fef51da56d9fcaec8e764aacb8de16.jpg
---

## Introduction

Write your blog post content here using standard **Markdown** syntax. The build script will convert this into a properly formatted HTML page.

## Headings

Use `##` for H2 headings (the most common in blog posts). The page title (H1) comes from the frontmatter.

### Subheadings

Use `###` for H3 subheadings if you need deeper structure.

## Text Formatting

- **Bold text** using `**double asterisks**`
- *Italic text* using `*single asterisks*`
- Regular paragraph text

## Links and Images

Add links like [this](https://example.com).

Add images:

![Alt text for the image](/images/blog/your-image.jpg)

The image path should point to a file in `site/www.milo.me/images/blog/`.

## Lists

Unordered list:
- Item one
- Item two
- Item three

Ordered list:
1. First step
2. Second step
3. Third step

## Code

Inline code: `const x = 42`

Code block:

```javascript
function greet(name) {
  return `Hello, ${name}!`;
}
```

## Blockquotes

> This is a blockquote. Use it for highlighting important quotes or callouts.

## Horizontal Rules

Use `---` to create a divider between sections.

---

That's it! Run `node build-post.js posts/example.md` to generate the HTML files.
