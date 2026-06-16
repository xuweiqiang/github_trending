# GitHub Trending Top20 抓取与展示

抓取 GitHub 过去 24 小时（Trending daily）Stars 增长 Top20，并通过 GitHub Pages 展示结果。

## 功能

- 抓取 GitHub Trending daily 页面
- 解析仓库名称、24h 增长、总 Stars、语言、描述
- 导出 `data/trending_24h.json` 与 `data/trending_24h.md`
- GitHub Actions 每小时自动更新并提交数据
- 自动部署静态网页，展示榜单摘要、搜索过滤和原始数据入口

## 本地运行

需要 Python 3.11 或更新版本。

```bash
pip install -r requirements.txt
python3 scripts/export_trending.py
```

## 本地预览网页

静态页面位于 `site/index.html`，页面运行时读取 `data/trending_24h.json`。建议用本地 HTTP 服务预览：

```bash
python3 -m http.server 8000
```

然后打开：

```text
http://127.0.0.1:8000/site/
```

## CI

工作流文件：

- `.github/workflows/github-trending-24h.yml`

触发方式：

- 手动触发 `workflow_dispatch`
- 每小时自动运行一次

工作流会执行以下动作：

1. 安装依赖并运行 `python scripts/export_trending.py`
2. 如数据变化，自动提交 `data/trending_24h.json` 与 `data/trending_24h.md`
3. 打包 `site/index.html` 和 `data/` 数据文件
4. 部署到 GitHub Pages

## 部署说明

仓库首次启用网页展示时，需要在 GitHub 仓库设置中打开 Pages：

1. 进入 `Settings` -> `Pages`
2. `Build and deployment` 的 `Source` 选择 `GitHub Actions`
3. 手动运行一次 `Update GitHub Trending 24h` workflow，或等待下一次整点后 5 分自动运行

部署成功后，网页地址通常为：

```text
https://<用户名或组织名>.github.io/<仓库名>/
```
