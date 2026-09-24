#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""看板数据与页面完整性测试。

用法：python tests/verify.py
校验项：
  1. data/tasks.json 结构合法（updated_at / tasks 字段存在）
  2. 每条命题记录含必要字段，数值类型正确
  3. 仅含推荐命题（技术课题 / 三方库），无自选命题混入
  4. index.html 引用的数据路径与展示列与数据字段一致
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAILS = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


# 1. 数据文件存在且结构合法
data_path = ROOT / "data" / "tasks.json"
check("data/tasks.json exists", data_path.is_file())
if data_path.is_file():
    data = json.loads(data_path.read_text(encoding="utf-8"))
    check("top-level fields", "updated_at" in data and "tasks" in data)
    tasks = data.get("tasks", [])

    # 2. 记录字段与类型
    required = {"type", "project_name", "participating", "submitted"}
    bad = [t for t in tasks if not required.issubset(t)
           or not isinstance(t["participating"], int)
           or not isinstance(t["submitted"], int)]
    check(f"all {len(tasks)} task records valid", not bad, f"{len(bad)} bad")

    # 3. 仅推荐命题
    types = {t["type"] for t in tasks}
    check("only recommended task types", types <= {"技术课题", "三方库"}, str(types))
    check("tech topics present", any(t["type"] == "技术课题" for t in tasks))
    check("libs present", any(t["type"] == "三方库" for t in tasks))

    # 4. index.html 与数据一致
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    check("index fetches data/tasks.json", "data/tasks.json" in html)
    for field in ("project_name", "type", "participating", "submitted"):
        check(f"index uses field .{field}", field in html)
    check("index has type filters", "技术课题" in html and "三方库" in html)

    print(f"\nsummary: {len(tasks)} recommended tasks | "
          f"registered {sum(t['participating'] for t in tasks)} | "
          f"submitted {sum(t['submitted'] for t in tasks)}")

sys.exit(1 if FAILS else 0)
