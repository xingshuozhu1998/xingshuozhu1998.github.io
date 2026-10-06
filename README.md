# 我的学习站点

主页：<https://xingshuozhu1998.github.io/>。这是公开项目的网站目录，每个入口同时提供网站链接和仓库链接。当前收录 LLM Atlas、Lilian Weng 中文阅读站、Linux C 编程一站式学习；主页自身的仓库在页脚提供入口。

## 自动收录

浏览器打开主页时查询账号的公开仓库，收录 `has_pages=true`（已经启用 GitHub Pages）的项目。已有三个项目保留审核过的中文介绍，新项目使用仓库名和仓库简介，按 `https://xingshuozhu1998.github.io/仓库名/` 建立入口。关闭 Pages 的项目会从成功同步后的目录中移除；私有仓库不会展示。

页面同时保留核实过的静态入口，关闭 JavaScript 或 GitHub 匿名查询达到限额时仍可访问已有站点。浏览器不会包含任何登录令牌。

`sync_sites.py` 使用相同筛选规则将目录写回 `index.html`。GitHub Actions（GitHub 的自动任务服务）工作流位于 `.github/workflows/sync-and-deploy.yml`，每小时第23分钟同步一次（`23 * * * *`），也支持手动运行和主页源码更新后运行。维护者已补齐 `workflow` 权限，Pages 发布源已切换为 GitHub Actions。打开主页时的自动发现也保留，不依赖定时任务。

自动任务使用 GitHub 提供的 `GITHUB_TOKEN`（只在运行时提供给任务的令牌），查询公开仓库、保存目录变化，并显式发布 Pages；这样可以避免自动提交不触发分支式 Pages 发布的问题。无需额外存储个人访问令牌。请求失败时任务报错，保留上一次已发布的内容。

## 限额与更新时间

每次查询最多读取100个仓库，超过100个时自动翻页。目前一次同步只需一条仓库列表请求。匿名查询的主限额为每IP每小时60次；Actions 自带令牌通常为每个仓库每小时1000次。当前每小时同步的列表查询用量约为每天24次，远低于后台限额。

GitHub 的定时任务可能延迟。公开仓库连续60天无活动时，定时任务会被平台暂停，需要在 Actions 页面重新启用；浏览器打开主页时的自动发现仍独立运行。

依据：[GitHub API限额](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api)、[定时任务规则](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)。

## 本地查看与同步

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

在浏览器打开 `http://127.0.0.1:8000/`。同步公开目录可运行 `python3 sync_sites.py`；匿名接口受共享IP限额影响时，可在本机环境变量 `GITHUB_TOKEN` 中提供授权，令牌不要写入代码或提交。

中文名称、介绍、主题标签和排列顺序保存在 `index.html` 的 `knownSites` 对象中。定时同步只替换 `sites:start` 与 `sites:end` 之间的卡片，以及站点数量，不改变主页设计。

## 已完成验收

主页已公开上线，HTTP 200，页面内容与本地版本一致；三个项目网站均返回 HTTP 200。正式网站在桌面与390像素手机视口下通过浏览器检查，手机无横向溢出，JavaScript 错误为0。

自动发现使用模拟新增站点、超过100个仓库的分页、关闭Pages、私有仓库及主页自身等场景验证：新增公开站点自动出现，其余非目录项目不展示。模拟匿名API限额错误时，三个静态入口仍然保留。后台脚本已在真实公开仓库列表上运行，结果与三个已发布项目一致。

工作流上传权限已经补齐，正在进行后台同步与自动发布的实际运行验收；运行结果将在完成后记录于此。
