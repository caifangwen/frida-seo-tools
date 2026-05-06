#!/usr/bin/env node

/**
 * 批量 JSON-LD 生成器
 * 从 input-files/ 读取文档，生成多种 JSON-LD Schema 输出
 */

const fs = require('fs').promises;
const path = require('path');
const JsonLdGenerator = require('./jsonld-generator');

const INPUT_DIR = path.join(__dirname, 'input-files');
const OUTPUT_DIR = path.join(__dirname, 'output-jsonld');

/**
 * 读取文件内容
 */
async function readFile(filepath) {
  try {
    return await fs.readFile(filepath, 'utf-8');
  } catch (error) {
    console.error(`❌ 读取失败: ${filepath}`, error.message);
    return null;
  }
}

/**
 * 处理单个文件
 */
async function processFile(filename) {
  const filepath = path.join(INPUT_DIR, filename);
  const ext = path.extname(filename).toLowerCase();
  
  console.log(`\n${'─'.repeat(60)}`);
  console.log(`📝 处理: ${filename}`);
  console.log('─'.repeat(60));

  // 读取文件
  const content = await readFile(filepath);
  if (!content) return null;

  // 创建生成器实例
  const generator = new JsonLdGenerator();

  // 解析内容
  if (ext === '.html') {
    await generator.parseHtml(content);
  } else if (ext === '.md' || ext === '.txt') {
    await generator.parseMarkdown(content);
  }

  console.log(`✓ 解析完成`);
  console.log(`  标题: ${generator.content.title}`);
  console.log(`  描述: ${generator.content.description.slice(0, 80)}...`);
  console.log(`  FAQ 数量: ${generator.content.faqs.length}`);

  // 生成所有 Schema
  const schemas = generator.generateAllSchemas();
  console.log(`✓ 生成了 ${Object.keys(schemas).length} 个 Schema:`);
  Object.keys(schemas).forEach(name => {
    console.log(`  ✓ ${name}`);
  });

  // 创建输出目录
  const outputSubDir = path.join(OUTPUT_DIR, filename.replace(/\.[^/.]+$/, ''));
  await fs.mkdir(outputSubDir, { recursive: true });

  // 输出方式 1: 完整的 HTML 文件（包含所有 JSON-LD 脚本标签）
  const htmlOutput = generator.toHtmlScriptTags(schemas);
  const htmlFile = path.join(outputSubDir, 'jsonld-scripts.html');
  await fs.writeFile(htmlFile, htmlOutput, 'utf-8');
  console.log(`✓ 已生成: jsonld-scripts.html`);

  // 输出方式 2: 单独的 JSON 文件
  const jsonFiles = generator.toJsonFiles(schemas);
  for (const [jsonFilename, jsonContent] of Object.entries(jsonFiles)) {
    const jsonFilepath = path.join(outputSubDir, jsonFilename);
    await fs.writeFile(jsonFilepath, jsonContent, 'utf-8');
    console.log(`✓ 已生成: ${jsonFilename}`);
  }

  // 输出方式 3: 合并的 JSON 文件
  const mergedFile = path.join(outputSubDir, 'all-schemas.json');
  await fs.writeFile(mergedFile, JSON.stringify(schemas, null, 2), 'utf-8');
  console.log(`✓ 已生成: all-schemas.json`);

  // 输出方式 4: 完整的 HTML 示例文件（集成到 HTML 中）
  const fullHtml = generateFullHtml(generator, schemas);
  const fullHtmlFile = path.join(outputSubDir, 'complete-example.html');
  await fs.writeFile(fullHtmlFile, fullHtml, 'utf-8');
  console.log(`✓ 已生成: complete-example.html`);

  return {
    filename,
    schemas: Object.keys(schemas),
    outputDir: outputSubDir
  };
}

/**
 * 生成完整的 HTML 示例
 */
function generateFullHtml(generator, schemas) {
  const schemaScripts = generator.toHtmlScriptTags(schemas);
  
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${generator.content.title}</title>
  <meta name="description" content="${generator.content.description}">
  
  ${schemaScripts}
</head>
<body>
  <article>
    <h1>${generator.content.title}</h1>
    <p>${generator.content.description}</p>
    
    ${generator.content.faqs.length > 0 ? `
    <section id="faq">
      <h2>FAQ</h2>
      ${generator.content.faqs.map(faq => `
      <div class="faq-item">
        <h3>${faq.question}</h3>
        <p>${faq.answer}</p>
      </div>
      `).join('\n')}
    </section>
    ` : ''}
  </article>
</body>
</html>`;
}

/**
 * 批量处理所有文件
 */
async function batchProcess() {
  console.log('╔═══════════════════════════════════════════════════════════╗');
  console.log('║         🚀  JSON-LD Schema 批量生成器                   ║');
  console.log('║         从文档生成多种 JSON-LD 结构化数据                ║');
  console.log('╚═══════════════════════════════════════════════════════════╝\n');

  // 读取输入文件
  let files;
  try {
    files = await fs.readdir(INPUT_DIR);
  } catch (error) {
    console.error(`❌ 输入目录不存在: ${INPUT_DIR}`);
    process.exit(1);
  }

  // 过滤支持的文件类型
  files = files.filter(f => /\.(html|md|txt)$/i.test(f));
  
  if (files.length === 0) {
    console.log('⚠️  没有找到支持的文件');
    process.exit(0);
  }

  console.log(`📁 找到 ${files.length} 个文件:\n`);
  files.forEach((f, i) => console.log(`  ${i + 1}. ${f}`));

  // 创建输出目录
  await fs.mkdir(OUTPUT_DIR, { recursive: true });

  // 处理每个文件
  const results = [];
  for (const filename of files) {
    const result = await processFile(filename);
    if (result) results.push(result);
  }

  // 输出总结
  console.log('\n\n' + '═'.repeat(60));
  console.log('🎉 批量生成完成！');
  console.log('═'.repeat(60));
  console.log(`\n📊 统计:`);
  console.log(`   处理文件: ${results.length} 个`);
  console.log(`   输出目录: ${OUTPUT_DIR}`);
  
  console.log('\n📁 生成的文件:');
  results.forEach((r, i) => {
    console.log(`\n  ${i + 1}. ${r.filename}`);
    console.log(`     Schemas: ${r.schemas.join(', ')}`);
    console.log(`     位置: ${r.outputDir}`);
    
    // 列出生成的文件
    fs.readdir(r.outputDir).then(files => {
      files.forEach(f => console.log(`       - ${f}`));
    });
  });

  console.log('\n💡 输出格式说明:');
  console.log('   ✓ jsonld-scripts.html - 可直接嵌入网站的 JSON-LD 脚本');
  console.log('   ✓ *-schema.json - 单独的 JSON Schema 文件');
  console.log('   ✓ all-schemas.json - 所有 Schema 的合并文件');
  console.log('   ✓ complete-example.html - 完整的 HTML 示例');
  console.log();
}

// 运行批量处理
batchProcess().catch(error => {
  console.error('\n❌ 处理失败:', error);
  process.exit(1);
});
