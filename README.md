# 数学三书学习站

把《什么是数学》《数学手册》《普林斯顿数学指南》三本书做成的一套可开学知识库。三本整合成一门课：24 章精讲、24 个概念页、57 道测验（含 9 道跨书综合题）、120 张抽认卡、94 条术语，收在一个 `index.html` 里，可以直接挂 GitHub Pages。

## 打开就能学

双击根目录的 `index.html`，浏览器会打开总学习手册。不需要服务器，不需要联网，所有内容都在这一个文件里。

顶部切换三本书与跨书总览，左侧按书导航（路径 / 章节 / 概念 / 测验 / 卡片 / 术语 / 模式 / 速查），搜索框覆盖全部书，进度存在浏览器本地，关掉再开会接着上次。

每本书另有一个独立的单文件伴侣，可以单独发给别人：

- `01-什么是数学/what-is-mathematics学习伴侣.html`
- `02-数学手册/bronstein-handbook学习伴侣.html`
- `03-普林斯顿数学指南/princeton-guide学习伴侣.html`

## 目录结构

```
数学三书学习站/
├── index.html                总学习手册（单文件，离线可用）
├── index.md                  Markdown 导航页
├── README.md                 本文件
├── .nojekyll                 GitHub Pages 关闭 Jekyll
├── 00-跨书总览/              推荐顺序 / 概念映射 / 综合检验
├── 01-什么是数学/            该书知识库 + 伴侣 HTML + manifest
├── 02-数学手册/
├── 03-普林斯顿数学指南/
└── _build/                   生成脚本与验证报告
```

每本书目录内部结构相同：

```
NN-书名/
├── SKILL.md                  学习总纲（心智模型 + 路径 + 章节索引）
├── chapters/                 8 章精讲
├── concepts/                 8 个概念页
├── paths/learn.md            八周学习路径
├── manifest.json             结构化清单（组装 HTML 用）
├── patterns.md               模式与框架
├── cheatsheet.md             速查表
├── quiz.md / flashcards.md / glossary.md
├── <slug>学习伴侣.html       单书伴侣
└── _work/raw/                抽取的分章原文
```

## 推荐学习顺序

1. 《什么是数学》——先建立"为什么这一步成立"的判断力。
2. 《数学手册》——有了推理习惯再学怎么算，公式才不变成死记。
3. 《普林斯顿数学指南》——最后读，才知道前面学的每一块在地图上什么位置。

二十四周走完，每周 6—8 小时。详细依据见 `00-跨书总览/README.md`。

## 部署到 GitHub Pages

三步：

```bash
# 1. 建仓库，把本目录内容放到仓库根目录（index.html 必须在根）
git init
git add .
git commit -m "数学三书学习站"
git branch -M main
git remote add origin https://github.com/<你的用户名>/<仓库名>.git
git push -u origin main
```

2. 打开仓库的 Settings → Pages，Source 选 `Deploy from a branch`，Branch 选 `main`，目录选 `/ (root)`，保存。

3. 等一两分钟，访问 `https://<你的用户名>.github.io/<仓库名>/`。

**`.nojekyll` 必须一起上传。** 没有它，Jekyll 会以 `_` 开头的目录（`_build/`、各书的 `_work/`）为理由拒绝托管，中文文件名也可能出问题。

## 常见问题

**页面打开是空白。** 检查是不是把 `index.html` 放进了子目录。它必须在站点根目录，或者你直接用本地文件路径打开。

**Mermaid 图不显示。** 总入口和伴侣页都从 CDN 加载 Mermaid，离线时会退化成源码文本。想完全离线看图，把 Mermaid 的 JS 文件下载到本地并改成本地引用。

**进度丢了。** 进度存在浏览器的 localStorage 里。换浏览器、清缓存、用无痕窗口都会丢，这是本地存储的固有限制。

**公式显示成代码块的样子。** 这是有意为之：生成脚本的 Markdown 渲染不解析 `$...$`，所有公式统一写成反引号内联代码，保证在任何环境下都能读。

## 内容边界

- 三本书各取 8 章，不是全书。取舍依据写在每本书 `SKILL.md` 的开头。
- 《普林斯顿数学指南》是扫描版，正文内容依靠 OCR 抽取后人工写作，个别页码的细节可能与原书有出入。发现疑点以原书为准。
- 三本书的解读与图示是本学习站新增的，原书没有。

## 重新生成

改动 Markdown 或 `manifest.json` 后，需要重跑组装，否则 HTML 与源文件会不一致：

```bash
python3 _build/gen_kb_docs.py 01-什么是数学         # 从 manifest 重生成 quiz/flashcards/glossary
python3 scripts/build_companion.py --manifest 01-什么是数学/manifest.json \
    --out 01-什么是数学/what-is-mathematics学习伴侣.html
python3 scripts/build_handbook.py --root . --order "01,02,03" --cross-dir 00-跨书总览
```

脚本在 `~/.doubao/agent_mode/workspace/.user_skills/book-enlighten/scripts/`。`verify_handbook.py` 可以跑端到端验证，当前 29 项全部通过。
