# GitHub Trending Top20 抓取

仅保留 GitHub 过去 24 小时（Trending daily）Stars 增长 Top20 抓取能力。

## 功能

- 抓取 GitHub Trending daily 页面
- 解析仓库名称、24h 增长、总 Stars、语言、描述
- 导出 `data/trending_24h.json` 与 `data/trending_24h.md`
- GitHub Actions 每小时自动更新并提交数据

## 本地运行

```bash
pip install -r requirements.txt
python scripts/export_trending.py
```

## CI

工作流文件：

- `.github/workflows/github-trending-24h.yml`

触发方式：

- 手动触发 `workflow_dispatch`
- 每小时自动运行一次
