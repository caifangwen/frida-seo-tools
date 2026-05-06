#!/usr/bin/env node

/**
 * JSON-LD Schema 生成器
 * 从 HTML/MD 文档中提取内容，生成多种 JSON-LD 结构化数据
 */

const fs = require('fs').promises;
const path = require('path');

class JsonLdGenerator {
  constructor() {
    this.schemas = [];
    this.content = {
      title: '',
      description: '',
      url: '',
      images: [],
      faqs: [],
      author: '',
      organization: '',
      datePublished: '',
      dateModified: '',
      keywords: [],
      breadcrumbs: [],
      products: [],
      articles: []
    };
  }

  /**
   * 从 HTML 内容中解析和提取信息
   */
  async parseHtml(content) {
    // 提取标题
    const titleMatch = content.match(/<title[^>]*>([^<]+)<\/title>/i);
    this.content.title = titleMatch ? titleMatch[1].trim() : 'Untitled';

    // 提取描述
    const descMatch = content.match(/<meta\s+name="description"\s+content="([^"]+)"/i);
    this.content.description = descMatch ? descMatch[1].trim() : '';

    // 提取关键词
    const kwMatch = content.match(/<meta\s+name="keywords"\s+content="([^"]+)"/i);
    if (kwMatch) {
      this.content.keywords = kwMatch[1].split(',').map(k => k.trim());
    }

    // 提取已有的 JSON-LD
    this.extractExistingJsonLd(content);

    // 提取 FAQ
    this.extractFaqs(content);

    // 提取日期
    const dateMatch = content.match(/(\d{4}-\d{2}-\d{2})/);
    if (dateMatch) {
      this.content.datePublished = dateMatch[1];
      this.content.dateModified = dateMatch[1];
    }

    return this.content;
  }

  /**
   * 提取已有的 JSON-LD
   */
  extractExistingJsonLd(content) {
    const jsonLdRegex = /<script\s+type="application\/ld\+json"[^>]*>([\s\S]*?)<\/script>/gi;
    let match;
    
    while ((match = jsonLdRegex.exec(content)) !== null) {
      try {
        const parsed = JSON.parse(match[1]);
        if (parsed['@type'] === 'Article') {
          this.content.author = parsed.author?.name || '';
          this.content.organization = parsed.publisher?.name || '';
        }
      } catch (e) {
        // 忽略解析错误
      }
    }
  }

  /**
   * 提取 FAQ
   */
  extractFaqs(content) {
    const faqRegex = /<script\s+type="application\/ld\+json"[^>]*>([\s\S]*?)<\/script>/gi;
    let match;
    
    while ((match = faqRegex.exec(content)) !== null) {
      try {
        const parsed = JSON.parse(match[1]);
        if (parsed['@type'] === 'FAQPage' && parsed.mainEntity) {
          this.content.faqs = parsed.mainEntity.map(q => ({
            question: q.name,
            answer: q.acceptedAnswer?.text || ''
          }));
        }
      } catch (e) {
        // 忽略解析错误
      }
    }
  }

  /**
   * 从 Markdown 解析内容
   */
  async parseMarkdown(content) {
    // 提取 frontmatter
    const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
    if (frontmatterMatch) {
      const frontmatter = frontmatterMatch[1];
      const titleMatch = frontmatter.match(/title:\s*["']?([^"'\n]+)["']?/i);
      const descMatch = frontmatter.match(/description:\s*["']?([^"'\n]+)["']?/i);
      
      if (titleMatch) this.content.title = titleMatch[1].trim();
      if (descMatch) this.content.description = descMatch[1].trim();
    }

    // 提取标题
    if (!this.content.title) {
      const h1Match = content.match(/^#\s+(.+)$/m);
      if (h1Match) this.content.title = h1Match[1].trim();
    }

    this.content.datePublished = new Date().toISOString().split('T')[0];
    this.content.dateModified = this.content.datePublished;

    return this.content;
  }

  /**
   * 生成 Article Schema
   */
  generateArticleSchema() {
    return {
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": this.content.title,
      "description": this.content.description,
      "datePublished": this.content.datePublished,
      "dateModified": this.content.dateModified,
      "author": {
        "@type": "Organization",
        "name": this.content.author || this.content.organization || "Your Company"
      },
      "publisher": {
        "@type": "Organization",
        "name": this.content.organization || "Your Company",
        "logo": {
          "@type": "ImageObject",
          "url": "https://www.yourdomain.com/logo.png"
        }
      },
      "mainEntityOfPage": {
        "@type": "WebPage",
        "@id": this.content.url || "https://www.yourdomain.com/page"
      },
      "image": this.content.images.length > 0 ? {
        "@type": "ImageObject",
        "url": this.content.images[0],
        "width": 1200,
        "height": 675
      } : undefined,
      "keywords": this.content.keywords.length > 0 ? this.content.keywords.join(', ') : undefined
    };
  }

  /**
   * 生成 FAQ Schema
   */
  generateFaqSchema() {
    if (this.content.faqs.length === 0) {
      return null;
    }

    return {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": this.content.faqs.map(faq => ({
        "@type": "Question",
        "name": faq.question,
        "acceptedAnswer": {
          "@type": "Answer",
          "text": faq.answer
        }
      }))
    };
  }

  /**
   * 生成 BreadcrumbList Schema
   */
  generateBreadcrumbSchema() {
    return {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "https://www.yourdomain.com/"
        },
        {
          "@type": "ListItem",
          "position": 2,
          "name": "Blog",
          "item": "https://www.yourdomain.com/blog"
        },
        {
          "@type": "ListItem",
          "position": 3,
          "name": this.content.title,
          "item": this.content.url || "https://www.yourdomain.com/page"
        }
      ]
    };
  }

  /**
   * 生成 Organization Schema
   */
  generateOrganizationSchema() {
    return {
      "@context": "https://schema.org",
      "@type": "Organization",
      "name": this.content.organization || "Your Company",
      "url": this.content.url || "https://www.yourdomain.com",
      "logo": "https://www.yourdomain.com/logo.png",
      "sameAs": [
        "https://www.facebook.com/yourcompany",
        "https://twitter.com/yourcompany",
        "https://www.linkedin.com/company/yourcompany"
      ]
    };
  }

  /**
   * 生成 WebPage Schema
   */
  generateWebPageSchema() {
    return {
      "@context": "https://schema.org",
      "@type": "WebPage",
      "name": this.content.title,
      "description": this.content.description,
      "url": this.content.url || "https://www.yourdomain.com/page",
      "datePublished": this.content.datePublished,
      "dateModified": this.content.dateModified,
      "isPartOf": {
        "@type": "WebSite",
        "name": this.content.organization || "Your Website",
        "url": "https://www.yourdomain.com"
      }
    };
  }

  /**
   * 生成 Product Schema（如果内容涉及产品）
   */
  generateProductSchema(productName, productDescription) {
    return {
      "@context": "https://schema.org",
      "@type": "Product",
      "name": productName || this.content.title,
      "description": productDescription || this.content.description,
      "brand": {
        "@type": "Brand",
        "name": this.content.organization || "Your Brand"
      },
      "offers": {
        "@type": "AggregateOffer",
        "priceCurrency": "USD",
        "lowPrice": "10.00",
        "highPrice": "100.00",
        "offerCount": "100",
        "availability": "https://schema.org/InStock"
      }
    };
  }

  /**
   * 生成所有适用的 Schema
   */
  generateAllSchemas() {
    const schemas = {
      article: this.generateArticleSchema(),
      faq: this.generateFaqSchema(),
      breadcrumb: this.generateBreadcrumbSchema(),
      webpage: this.generateWebPageSchema(),
      organization: this.generateOrganizationSchema()
    };

    // 过滤掉 null 值
    return Object.fromEntries(
      Object.entries(schemas).filter(([_, v]) => v !== null)
    );
  }

  /**
   * 输出为 HTML 格式的 JSON-LD 脚本
   */
  toHtmlScriptTags(schemas) {
    let output = '<!-- JSON-LD Structured Data -->\n';
    
    for (const [name, schema] of Object.entries(schemas)) {
      output += `\n<!-- ${name.charAt(0).toUpperCase() + name.slice(1)} Schema -->\n`;
      output += '<script type="application/ld+json">\n';
      output += JSON.stringify(schema, null, 2);
      output += '\n</script>\n';
    }

    return output;
  }

  /**
   * 输出为单独的 JSON 文件
   */
  toJsonFiles(schemas) {
    const result = {};
    
    for (const [name, schema] of Object.entries(schemas)) {
      result[`${name}-schema.json`] = JSON.stringify(schema, null, 2);
    }

    return result;
  }
}

module.exports = JsonLdGenerator;
