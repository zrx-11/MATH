#!/usr/bin/env python3
"""从 manifest.json 生成 quiz.md / flashcards.md / glossary.md。

用法： python3 gen_kb_docs.py <book_dir>
说明：这三份 Markdown 是知识库读物，内容与 manifest 同源，不手写，避免两处不一致。
"""
import json
import os
import sys

BOOK_DIR = sys.argv[1]
M = json.load(open(os.path.join(BOOK_DIR, "manifest.json"), encoding="utf-8"))
CHAPTERS = M["chapters"]
TITLE = {c["id"]: c["title"] for c in CHAPTERS}

# ---------- quiz.md ----------
lines = [f"# {M['title']} 测验", ""]
for ch in CHAPTERS:
    qs = [q for q in M.get("quizzes", []) if q.get("chapterId") == ch["id"]]
    if not qs:
        continue
    lines.append(f"## {ch['title']}（检查点）")
    lines.append("")
    for i, q in enumerate(qs, 1):
        kind = {"single": "单选", "multi": "多选", "blank": "填空"}.get(q["type"], q["type"])
        lines.append(f"### Q{i}.（{kind}）{q['question']}")
        if q.get("options"):
            for j, opt in enumerate(q["options"]):
                lines.append(f"- {chr(65 + j)}. {opt}")
        ans = q["answer"]
        if isinstance(ans, list):
            ans_txt = "、".join(chr(65 + x) for x in ans)
        elif q["type"] == "single" and isinstance(ans, int):
            ans_txt = chr(65 + ans)
        else:
            ans_txt = str(ans)
        lines.append(f"**答案**：{ans_txt}")
        lines.append(f"**解析**：{q.get('explain', '')}")
        lines.append("")
all_q = [q for q in M.get("quizzes", []) if q.get("chapterId") == "__all"]
if all_q:
    lines.append("## 综合测验（多章联考）")
    lines.append("")
    for i, q in enumerate(all_q, 1):
        kind = {"single": "单选", "multi": "多选", "blank": "填空"}.get(q["type"], q["type"])
        lines.append(f"### Q{i}.（{kind}）{q['question']}")
        for j, opt in enumerate(q.get("options") or []):
            lines.append(f"- {chr(65 + j)}. {opt}")
        ans = q["answer"]
        ans_txt = chr(65 + ans) if isinstance(ans, int) else str(ans)
        lines.append(f"**答案**：{ans_txt}")
        lines.append(f"**解析**：{q.get('explain', '')}")
        lines.append("")
lines.append("## 最终检验")
lines.append("")
lines.append("任选一个本书未出现的初等命题，写出从定义出发的完整证明，逐步标注依据。评分要点：命题陈述清楚、每步都有出处、没有跳步、结论回扣定义。")
open(os.path.join(BOOK_DIR, "quiz.md"), "w", encoding="utf-8").write("\n".join(lines))

# ---------- flashcards.md ----------
lines = [f"# {M['title']} 抽认卡", ""]
for ch in CHAPTERS:
    cards = [c for c in M.get("flashcards", []) if c.get("chapterId") == ch["id"]]
    if not cards:
        continue
    lines.append(f"## {ch['title']}")
    lines.append("")
    for c in cards:
        lines.append(f"### 卡片：{c['front']}")
        lines.append(f"- **背面**：{c['back']}")
        lines.append(f"- **标签**：{', '.join(c.get('tags', []))}")
        lines.append(f"- **章节**：{c['chapterId']}")
        lines.append("")
open(os.path.join(BOOK_DIR, "flashcards.md"), "w", encoding="utf-8").write("\n".join(lines))

# ---------- glossary.md ----------
lines = ["# 术语表", "", "| 术语 | 白话定义 | 首次出现 |", "|---|---|---|"]
for g in M.get("glossary", []):
    ch = TITLE.get(g.get("chapterId", ""), "—")
    lines.append(f"| {g['term']} | {g['def']} | {ch} |")
open(os.path.join(BOOK_DIR, "glossary.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")

print(f"OK {BOOK_DIR}: quiz {len(M.get('quizzes', []))} / cards {len(M.get('flashcards', []))} / terms {len(M.get('glossary', []))}")
