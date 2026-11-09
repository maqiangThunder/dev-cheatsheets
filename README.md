# 开发者速查表 · Developer Cheat Sheets

三个最常被翻来翻去的表的纯静态中文版：

- **ASCII 码表** — 0–127 全码位，十进制 / 十六进制 / 字符 / 含义，含控制字符与转义坑
- **HTTP 状态码** — 1xx–5xx 全量中文对照，含 401/403、301/302/303/307/308、502/504 辨析
- **Cron 表达式** — 5 字段语法、特殊符号、20+ 常用写法、四个经典陷阱

线上地址：<https://maqiangthunder.github.io/dev-cheatsheets/>

## 特点

- 纯静态单文件 HTML，样式内联，无外部依赖，可离线保存
- 无广告、无登录、无追踪脚本
- 支持深色模式（跟随系统）
- 表格数据可直接选中复制

## 结构

```
build.py            # 生成脚本（内容与模板都在这里）
docs/               # 生成产物，GitHub Pages 直接发布此目录
  index.html
  ascii/index.html
  httpstatus/index.html
  cron/index.html
  robots.txt
  sitemap.xml
```

## 本地构建

```bash
python3 build.py
```

改内容 → 改 `build.py` → 重跑。脚本是幂等的，整份重写 `docs/*.html`。

## 数据来源

- ASCII：ANSI X3.4-1968 / ISO 646
- HTTP 状态码：IANA HTTP Status Code Registry、RFC 9110
- Cron：以 Vixie Cron 实现为基准（Linux crontab 与多数在线 Cron 服务使用的方言）

发现错漏欢迎提 Issue。

## License

文档内容 CC BY 4.0，生成脚本 MIT。
