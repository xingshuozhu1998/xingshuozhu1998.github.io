#!/usr/bin/env python3
"""从公开仓库列表同步启用了 Pages 的项目，保留主页中审核过的中文介绍。"""
import html
import json
import os
import re
import urllib.request
from pathlib import Path

OWNER = 'xingshuozhu1998'
ROOT = Path(__file__).resolve().parent


def fetch_repositories():
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'github-pages-directory'}
    if os.environ.get('GITHUB_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GITHUB_TOKEN']
    repos = []
    page = 1
    while True:
        request = urllib.request.Request(f'https://api.github.com/users/{OWNER}/repos?per_page=100&page={page}', headers=headers)
        with urllib.request.urlopen(request, timeout=30) as response:
            batch = json.load(response)
        repos.extend(batch)
        if len(batch) < 100:
            return repos
        page += 1


def render_card(repo, info, index):
    esc = html.escape
    url = f'https://{OWNER}.github.io/{repo["name"]}/'
    tags = ''.join('<li>' + esc(tag) + '</li>' for tag in info['tags'])
    return f'''<article class="site-card {info['theme']}" data-repository="{esc(repo['name'], quote=True)}">
 <div class="card-visual" aria-hidden="true"><span class="visual-grid"></span><span class="visual-symbol">{esc(info['symbol'])}</span><span class="visual-number">{index:02d}</span></div>
 <div class="card-body"><p class="category">{esc(info['category'])}</p><h3>{esc(info['title'])}</h3><p class="description">{esc(info['description'])}</p><ul class="tags" aria-label="主题">{tags}</ul>
 <div class="card-links"><a class="visit" href="{esc(url, quote=True)}">访问网站 <span aria-hidden="true">↗</span></a><a class="repository" href="{esc(repo['html_url'], quote=True)}" target="_blank" rel="noopener noreferrer" aria-label="查看{esc(info['title'], quote=True)}的GitHub仓库">查看仓库 <span aria-hidden="true">↗</span></a></div></div></article>'''


def sync(repos):
    path = ROOT / 'index.html'
    source = path.read_text()
    known = json.loads(re.search(r'^const knownSites = (.*);$', source, re.M)[1])
    order = list(known)
    # 只展示账号自己的公开项目；主页自身的仓库入口在页脚，避免重复卡片。
    sites = [repo for repo in repos if repo['has_pages'] and not repo['private'] and repo['owner']['login'] == OWNER and repo['name'] != f'{OWNER}.github.io']
    sites.sort(key=lambda repo: (order.index(repo['name']) if repo['name'] in order else len(order), repo['name'].lower()))
    cards = []
    for index, repo in enumerate(sites, 1):
        info = known.get(repo['name'], {'title': repo['name'], 'category': '学习与项目', 'description': repo['description'] or '浏览这个项目的公开网站。', 'theme': 'blue', 'symbol': '↗', 'tags': []})
        cards.append(render_card(repo, info, index))
    # 查询成功后才更新页面；请求失败会直接使同步任务失败，保留已部署的完整目录。
    source = re.sub(r'<!-- sites:start -->[\s\S]*?<!-- sites:end -->', lambda match: '<!-- sites:start -->\n' + '\n'.join(cards) + '\n<!-- sites:end -->', source)
    source = re.sub(r'(<span id="site-count" class="site-count">).*?(</span>)', lambda match: match[1] + str(len(sites)) + ' 个站点' + match[2], source)
    path.write_text(source)
    return [repo['name'] for repo in sites]


if __name__ == '__main__':
    print('已同步公开站点：' + '、'.join(sync(fetch_repositories())))
