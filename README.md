# 仓颉生态创新开发挑战赛 · 推荐命题数据看板

大赛作业：推荐命题数据看板——可查看各推荐命题的**已报名团队数**与**提交作品数量**，供参赛者选题时参考。

## 在线访问

- GitHub Pages（推荐，代理/直连均可）：<https://wanglin1111111.github.io/cj-dashboard/>
- Surge 镜像（国内直连可用）：<https://cj-dashboard.surge.sh/>

## 在线数据源

- 官方看板：<https://scoreboard.atomgit.com/>
- 数据接口：`https://scoreboard.atomgit.com/api/dashboard/summary`

## 本地使用

```bash
# 1. 刷新数据快照（可选，仓库已含 data/tasks.json）
curl -s https://scoreboard.atomgit.com/api/dashboard/summary | python -c "
import json,sys
d=json.load(sys.stdin)
rec=[t for t in d['task_participation'] if t['type'] in ('技术课题','三方库')]
json.dump({'updated_at':d['updated_at'],'tasks':rec},open('data/tasks.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
"

# 2. 本地起静态服务后访问
python -m http.server 8080
# 打开 http://localhost:8080
```

## 功能

- 顶部指标卡：推荐命题总数、报名团队总数、提交作品总数、技术课题/三方库分类汇总
- 按报名热度降序排列，报名 ≥4 的命题橙色高亮（提示同题竞争激烈）
- 命题类型筛选（技术课题 / 三方库）+ 关键词搜索
- 每个命题的报名数、提交数、提交率进度条

## 数据快照说明

仓库内 `data/tasks.json` 为 2026-09-24 的数据快照（82 个推荐命题）。官方接口出现「赛事接口鉴权失败 (HTTP 403)」期间，可使用快照离线浏览；接口恢复后按上方命令刷新即可。

## 技术栈

纯静态 HTML + 原生 JavaScript，无构建、无依赖，可直接托管到任意静态服务。

## LICENSE

MIT License（见 [LICENSE](LICENSE)）
