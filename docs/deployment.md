# 个人网站上线与 .me 域名

## 现在在哪里

2026-10-09：`Analalaa/Anle-site` 已切换为 GitHub Actions 自动发布。每次推送 `main` 会生成并发布网站，正式地址为 <https://anlening.me/>，中文首页为 <https://anlening.me/zh/index.html>。原 GitHub Pages 地址会跳转到正式域名。

网站通过 `.github/workflows/deploy-pages.yml` 自动发布。`site/www.milo.me` 只是历史目录名，不代表拥有 `milo.me`。该目录中的旧 Vercel 关联文件也不代表域名已购买或解析成功。

## 推荐路径：沿用 GitHub Pages

1. 在本地预览并确认中英文内容与下载包。
2. [仓库的 Pages 设置](https://github.com/Analalaa/Anle-site/settings/pages) 中 Build and deployment → Source 已设为 **GitHub Actions**。
3. 将本次确认后的源码、生成页面、下载包及 `.github/workflows/deploy-pages.yml` 提交并推送到 `main`。
4. 在 Actions 中查看 **Publish personal site**，成功后访问正式域名。需要重发时可手动 Run workflow。

工作流重新生成静态 HTML，读取 Pages 实际网址，然后导出并发布。它会为默认地址加上 `/Anle-site` 前缀；绑定个人域名后使用域名根路径。导航、图片、下载、旧页面跳转和 RSS 随实际网址更新。更改域名后须重新运行工作流一次。

本地验证导出：

```bash
python3 scripts/build_site.py
python3 scripts/export_site.py --output _site --base-url https://anlening.me
```

导出目标必须是不存在的新目录，以免覆盖已有文件。可换一个新目录重新验证；普通本机预览仍直接使用 `site/www.milo.me`。工作流无需额外付费服务或自建服务器，也不需要把私有访问凭据放进仓库。

工作流参考：[GitHub 自定义 Pages 工作流](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)、[configure-pages 网址输出](https://github.com/actions/configure-pages/blob/v5/action.yml)。

## 接入自己的 .me

正式域名：`anlening.me`，注册商与 DNS 服务为 Spaceship。2026-10-09 已完成 GitHub Pages 域名绑定及下表的五条解析记录。主域名证书已获批准，并已开启 **Enforce HTTPS**。证书由 GitHub Pages 管理，无需在 Spaceship 购买 SSL 或主机。

上线验证：主域名的中英文首页、小作品页、样式、脚本、Prompts ZIP 与 Recoding APK 均已实际访问核对。`www.anlening.me` 配置为指向 `analalaa.github.io`，由 GitHub Pages 处理跳转。

以下配置适用于 `anlening.me`，并将 `www.anlening.me` 重定向到主域名：

1. 可选的账户级保护：在 GitHub 个人设置 → Pages 添加域名，按它给出的 TXT 记录验证归属。本次已完成仓库域名绑定，未配置账户级 TXT 验证。
2. 在仓库 Settings → Pages → Custom domain 填写域名并保存。
3. 在域名的 DNS 管理处配置下表。若选根域名为主站，同时配置 `www`，GitHub 会处理两者之间的跳转。
4. DNS 检查通过、证书准备好后，启用 **Enforce HTTPS**。DNS 与证书可能需要等待，官方说明最长可达 24 小时。
5. 重新运行发布工作流。用手机实际打开首页、作品详情、相册、RSS，以及 Prompts 与 Recoding 的下载链接。

| 类型 | 主机记录 | 值 |
| --- | --- | --- |
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | analalaa.github.io |

所有记录 TTL 为 30 分钟。Spaceship 可能将同一主机名的多条 A 记录提示为“Conflicting records”；这里的四个地址是 GitHub Pages 官方要求的地址，应一并保留。

`www` 的 CNAME 不带协议、不带 `/Anle-site`。TXT 验证值以 GitHub 实际给出的为准。只调整网站对应的记录，保留邮箱等其他用途的 DNS 记录。本工作流使用 Actions，不需要在源码中添加 CNAME 文件。

官方依据：[GitHub 自定义域名与 DNS](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)。

## 五个小作品怎样给人使用

| 作品 | 交付方式 | 当前状态 / 上线前工作 |
| --- | --- | --- |
| Prompts | 主页直接提供 ZIP 和安装说明 | 包已准备；访问者安装到自己的 Codex，索引自己的对话 |
| Date with me | 独立应用，主页链接过去 | 选中 `codex/pop-art-activity-selection` 分支的红黄蓝绿色块版；旧公开地址仍是白色版，新版上线前不把旧地址当作新版体验入口 |
| Mood Recipe | 独立 Node/Express 服务，主页链接过去 | 静态 Pages 不能运行该服务；需配置图像理解服务，并决定所有访客共享记录还是每人独立记录 |
| Color Muse | 直接链接已发布的网页 | <https://analalaa.github.io/color/> |
| Recoding · 随记 | 主页直接提供 Android APK | `0.6.1-device` 测试包，Android 8.0+；安装后本机使用，没有网页版或 iOS 版 |

Date 色块版源码位于本机 `dating/site`，分支为 `codex/pop-art-activity-selection`，本次确认的提交为 `41af04f`。已有 Sites 项目与数据库，应从这个分支更新原应用，保留已有预约数据。当前公开地址是 <https://date-with-me.caiwei625x.chatgpt.site>；只有确认发布后确实呈现色块版，再把该地址填回 `content/projects.json` 的 `url`，并删除“待发布”的中英文提示。单纯发布个人主页不会更新这个独立应用。

Mood Recipe 的源码是 `sail`。现有实现保存并向所有访客广播同一份记录；发布前需要明确产品行为。现有个人记录、服务密钥不应进入公开静态资源。服务部署并验证后，再配置作品的 `url`。

Recoding 安装包与源发布包 SHA-256 一致：`a0da14ea2f9152847e5a7072085237fb9407efcbcf00fd8c81a81334a4c685ef`。页面明确标为测试版，尚未声称完成真机体验验证或离线语音转文字。沿用现有测试签名；将来改为正式分发需先规划签名延续与更新方式。

个人 `.me` 主站可以先上线；独立应用继续使用各自已有地址，不需要等五个作品都迁到同一个服务器。
