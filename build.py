# -*- coding: utf-8 -*-
"""
生成 dev-cheatsheets 静态站到 docs/（GitHub Pages 直接发布 docs/ 目录）。

用法：
    python3 build.py

改内容 → 改本文件 → 重跑即可（幂等，整份重写 docs/*.html）。
"""
import os
import html

BASE_URL = "https://maqiangthunder.github.io/dev-cheatsheets"
UTIL = "https://util123.top"
SITE = "开发者速查表"
OUT = "docs"

CSS = r"""
:root{--brand:#2563eb;--brand-d:#1d4ed8;--accent:#0ea5e9;--ink:#0f172a;--muted:#64748b;
--line:#e2e8f0;--bg:#f8fafc;--card:#fff;--code-bg:#f1f5f9;--tip-bg:#eff6ff;--tip-line:#bfdbfe;
--warn-bg:#fff7ed;--warn-line:#fed7aa;--ok:#059669}
@media (prefers-color-scheme:dark){:root{--ink:#e2e8f0;--muted:#94a3b8;--line:#1e293b;
--bg:#0b1220;--card:#111a2b;--code-bg:#0f172a;--tip-bg:#0e1c33;--tip-line:#1e3a5f;
--warn-bg:#2a1c0c;--warn-line:#7c4a12;--ok:#34d399}}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
color:var(--ink);background:var(--bg);line-height:1.68;-webkit-font-smoothing:antialiased;font-size:15.5px}
.wrap{max-width:920px;margin:0 auto;padding:0 20px}
header{background:linear-gradient(135deg,#1d4ed8 0%,#0ea5e9 100%);color:#fff;padding:46px 0 40px}
header a{color:#dbeafe}
header h1{margin:8px 0 12px;font-size:31px;line-height:1.3;letter-spacing:-.4px}
header h1 .en{display:block;font-size:15px;font-weight:400;opacity:.82;margin-top:8px;letter-spacing:0}
header p.lead{margin:0;opacity:.93;font-size:15px;max-width:660px}
.crumb{font-size:13px;opacity:.85;text-decoration:none}
.crumb:hover{text-decoration:underline}
a.cta{display:inline-block;margin-top:20px;background:#fff;color:var(--brand-d);text-decoration:none;
font-weight:600;padding:11px 22px;border-radius:10px;font-size:14.5px;box-shadow:0 2px 10px rgba(2,6,23,.16)}
a.cta:hover{background:#f1f5f9}
main{padding:34px 0 56px}
section{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:22px 22px 10px;margin-bottom:20px}
h2{font-size:19.5px;margin:0 0 6px;letter-spacing:-.2px}
h2 .en{font-weight:400;color:var(--muted);font-size:13.5px;margin-left:8px;letter-spacing:0}
.sub{color:var(--muted);font-size:13.8px;margin:0 0 15px}
h3{font-size:15.5px;margin:20px 0 8px}
p{margin:0 0 12px}
ul,ol{margin:0 0 14px;padding-left:22px}
li{margin-bottom:6px}
code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.92em;
background:var(--code-bg);padding:1px 5px;border-radius:5px}
table{width:100%;border-collapse:collapse;font-size:14px;margin-bottom:16px}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-size:12.5px;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:.04em;
border-bottom:1px solid #cbd5e1;white-space:nowrap;position:sticky;top:0;background:var(--card)}
tbody tr:hover{background:var(--code-bg)}
td.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-weight:700;color:var(--brand);white-space:nowrap}
td.ch{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:15px;text-align:center}
.scroll{overflow-x:auto;-webkit-overflow-scrolling:touch}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px;margin-bottom:6px}
a.card{display:block;text-decoration:none;color:inherit;background:var(--card);border:1px solid var(--line);
border-radius:12px;padding:16px 18px;transition:.15s;margin-bottom:0}
a.card:hover{border-color:var(--brand);transform:translateY(-2px);box-shadow:0 6px 18px rgba(37,99,235,.12)}
a.card .t{font-weight:650;font-size:15.5px;margin-bottom:4px;color:var(--brand)}
a.card .d{font-size:13.4px;color:var(--muted);line-height:1.55}
.tip,.warn{border-radius:10px;padding:13px 16px;margin:0 0 16px;font-size:14px}
.tip{background:var(--tip-bg);border:1px solid var(--tip-line)}
.warn{background:var(--warn-bg);border:1px solid var(--warn-line)}
.tip b,.warn b{display:block;margin-bottom:3px}
.grp{font-weight:650;font-size:14px;margin:18px 0 6px;color:var(--muted)}
footer{border-top:1px solid var(--line);padding:26px 0 40px;color:var(--muted);font-size:13.4px}
footer a{color:var(--brand);text-decoration:none}
footer a:hover{text-decoration:underline}
footer .links{margin-bottom:8px}
@media(max-width:600px){
header{padding:34px 0 30px}header h1{font-size:24px}body{font-size:15px}
section{padding:18px 16px 6px}main{padding:24px 0 40px}
table{font-size:13.2px}th,td{padding:7px 8px}
}
"""


def esc(s):
    return html.escape(str(s), quote=True)


def shell(slug, title, desc, body, h1, en, lead, cta=None, extra_head=""):
    """slug 为空串表示首页。"""
    canonical = BASE_URL + "/" + (slug + "/" if slug else "")
    if slug:
        rel = "../"
        crumb = '<a class="crumb" href="../">← 开发者速查表</a>'
    else:
        rel = ""
        crumb = '<span class="crumb">开发者速查表 · Developer Cheat Sheets</span>'
    cta_html = ""
    if cta:
        cta_html = '<a class="cta" href="%s">%s →</a>' % (esc(cta[1]), esc(cta[0]))
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s">
<meta name="robots" content="index, follow">
<meta property="og:type" content="website">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:url" content="%s">
<meta name="theme-color" content="#2563eb">
<meta name="msvalidate.01" content="%s">
%s<style>%s</style>
</head>
<body>
<header>
  <div class="wrap">
    %s
    <h1>%s<span class="en">%s</span></h1>
    <p class="lead">%s</p>
    %s
  </div>
</header>
<main>
  <div class="wrap">
%s
  </div>
</main>
<footer>
  <div class="wrap">
    <div class="links">相关：<a href="%s" target="_blank" rel="noopener">Util123 在线工具集</a> · <a href="%sascii/">ASCII 码表</a> · <a href="%shttpstatus/">HTTP 状态码</a> · <a href="%scron/">Cron 表达式</a></div>
    <div>本站为纯静态速查手册，数据可自由引用。需要交互计算请使用 <a href="%s" target="_blank" rel="noopener">util123.top</a>。</div>
    <div style="margin-top:6px">© 2026 %s · <a href="https://github.com/maqiangThunder/dev-cheatsheets" target="_blank" rel="noopener">GitHub</a></div>
  </div>
</footer>
</body>
</html>
""" % (
        esc(title), esc(desc), esc(canonical), esc(title), esc(desc), esc(canonical),
        BING_MSVALIDATE, extra_head, CSS, crumb, h1, esc(en), lead, cta_html, body,
        UTIL, rel, rel, rel, UTIL, SITE,
    )


# ---------------------------------------------------------------- 首页
def build_index():
    cards = [
        ("ascii/", "ASCII 码表", "0–127 全码位对照：十进制 / 十六进制 / 字符 / 含义，含控制字符与常见转义坑。"),
        ("httpstatus/", "HTTP 状态码", "1xx–5xx 全量状态码中文速查 + 401/403、301/302/307/308、502/504 等易混辨析。"),
        ("cron/", "Cron 表达式", "5 字段语法、特殊符号含义、20+ 常用写法，以及月日与周同时指定这类经典陷阱。"),
    ]
    grid = "\n".join(
        '<a class="card" href="%s"><div class="t">%s</div><div class="d">%s</div></a>' % (u, t, d)
        for u, t, d in cards
    )
    body = """
<section>
  <h2>速查表目录<span class="en">Cheat Sheets</span></h2>
  <p class="sub">纯静态、无广告、无登录，手机上也能直接查。表格里的数据可以直接复制。</p>
  <div class="grid">
%s
  </div>
</section>

<section>
  <h2>为什么是「速查」而不是「工具」<span class="en">Why a reference, not a tool</span></h2>
  <p>查表是线性的：知道要找什么，只需要快速定位。这类场景下，一页纯静态 HTML 比任何需要加载、需要点选、需要联网调接口的工具都更快 —— 打开即到，Ctrl+F 就能搜。</p>
  <p>但有些问题查表解决不了。比如「这条 cron 下次什么时候跑」不是查出来的，是算出来的；「这段 Base64 解出来是什么」也不是查出来的。这些交给 <a href="https://util123.top" target="_blank" rel="noopener">util123.top</a> 上的在线工具。</p>
  <div class="tip"><b>两手准备</b>这里负责「记住写法」，工具站负责「验证结果」。速查页底部的按钮会直接跳到对应工具，不用自己找。</div>
</section>

<section>
  <h2>数据来源与维护<span class="en">Sources</span></h2>
  <ul>
    <li>ASCII 码表依据 ANSI X3.4-1968 / ISO 646 标准字符集整理。</li>
    <li>HTTP 状态码依据 IANA HTTP Status Code Registry 与 RFC 9110 整理。</li>
    <li>Cron 语法以 Vixie Cron 实现为基准 —— 这也是 Linux 发行版和大多数在线 Cron 服务实际使用的方言。</li>
  </ul>
  <p>发现错漏欢迎在 <a href="https://github.com/maqiangThunder/dev-cheatsheets/issues" target="_blank" rel="noopener">GitHub Issues</a> 提出。</p>
</section>
""" % grid
    return shell(
        "", "开发者速查表 · ASCII / HTTP 状态码 / Cron 表达式 | Developer Cheat Sheets",
        "中文开发者速查表：ASCII 码表、HTTP 状态码全量对照、Cron 表达式语法与常用示例。纯静态、无广告、可离线保存。",
        body,
        "开发者速查表",
        "ASCII · HTTP Status Codes · Cron Expressions",
        "三个最常被翻来翻去的表。纯静态页面，打开即查，不用等加载。",
        cta=("打开在线工具集", UTIL),
    )


# ---------------------------------------------------------------- ASCII
CTRL = {
    0: "NUL 空字符", 1: "SOH 标题开始", 2: "STX 正文开始", 3: "ETX 正文结束",
    4: "EOT 传输结束", 5: "ENQ 询问", 6: "ACK 确认", 7: "BEL 响铃",
    8: "BS 退格", 9: "HT 水平制表（Tab）", 10: "LF 换行（\\n）", 11: "VT 垂直制表",
    12: "FF 换页", 13: "CR 回车（\\r）", 14: "SO 移出", 15: "SI 移入",
    16: "DLE 数据链路转义", 17: "DC1 设备控制 1（XON）", 18: "DC2 设备控制 2",
    19: "DC3 设备控制 3（XOFF）", 20: "DC4 设备控制 4", 21: "NAK 否定应答",
    22: "SYN 同步空闲", 23: "ETB 块传输结束", 24: "CAN 取消", 25: "EM 介质结束",
    26: "SUB 替换", 27: "ESC 转义", 28: "FS 文件分隔符", 29: "GS 组分隔符",
    30: "RS 记录分隔符", 31: "US 单元分隔符",
}

CHAR_NAME = {
    32: "空格", 33: "叹号", 34: "双引号", 35: "井号", 36: "美元符", 37: "百分号",
    38: "与号", 39: "单引号", 40: "左圆括号", 41: "右圆括号", 42: "星号", 43: "加号",
    44: "逗号", 45: "连字符", 46: "句点", 47: "斜杠", 48: "数字 0", 49: "数字 1",
    50: "数字 2", 51: "数字 3", 52: "数字 4", 53: "数字 5", 54: "数字 6", 55: "数字 7",
    56: "数字 8", 57: "数字 9", 58: "冒号", 59: "分号", 60: "小于号", 61: "等号",
    62: "大于号", 63: "问号", 64: "at 符", 91: "左方括号", 92: "反斜杠",
    93: "右方括号", 94: "脱字符", 95: "下划线", 96: "反引号", 123: "左花括号",
    124: "竖线", 125: "右花括号", 126: "波浪号",
}


def ch_disp(code):
    if code == 32:
        return "␠"
    if code < 32:
        return "—"
    if code == 127:
        return "␡"
    return esc(chr(code))


def build_ascii():
    # 控制字符表
    rows_ctrl = []
    for i in range(0, 32):
        rows_ctrl.append(
            "<tr><td class=\"mono\">%d</td><td class=\"mono\">0x%02X</td><td>%s</td>"
            "<td>%s</td></tr>" % (i, i, ch_disp(i), esc(CTRL[i]))
        )
    ctrl_tbl = ("<div class=\"scroll\"><table><thead><tr><th>十进制</th><th>十六进制</th>"
                "<th>缩写</th><th>含义</th></tr></thead><tbody>%s</tbody></table></div>"
                % "".join(rows_ctrl))

    # 可打印字符：4 列并排展示 32-126，每列「十进制 / 十六进制 / 字符 / 名称」
    printable = list(range(32, 127))
    cols = 4
    per = (len(printable) + cols - 1) // cols
    chunks = [printable[i * per:(i + 1) * per] for i in range(cols)]
    head = "".join("<th>十进制</th><th>十六进制</th><th>字符</th><th>说明</th>" for _ in range(cols))
    body_rows = []
    for r in range(per):
        cells = []
        for c in chunks:
            if r < len(c):
                code = c[r]
                cells.append("<td class=\"mono\">%d</td><td class=\"mono\">0x%02X</td>"
                             "<td class=\"ch\">%s</td><td>%s</td>"
                             % (code, code, ch_disp(code), esc(CHAR_NAME.get(code, "—"))))
            else:
                cells.append("<td></td><td></td><td></td><td></td>")
        body_rows.append("<tr>%s</tr>" % "".join(cells))
    print_tbl = ("<div class=\"scroll\"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>"
                 % (head, "".join(body_rows)))

    # 常用转义对照
    esc_rows = [
        ("\\n", "LF", "0x0A", "换行，Unix/Linux/macOS 行尾"),
        ("\\r", "CR", "0x0D", "回车，经典 Mac 行尾"),
        ("\\r\\n", "CRLF", "0x0D 0x0A", "Windows 行尾，两个字节"),
        ("\\t", "HT", "0x09", "水平制表符"),
        ("\\0", "NUL", "0x00", "C 字符串结束符"),
        ("\\b", "BS", "0x08", "退格"),
        ("\\f", "FF", "0x0C", "换页"),
        ("\\v", "VT", "0x0B", "垂直制表"),
    ]
    esc_tbl = ("<div class=\"scroll\"><table><thead><tr><th>转义写法</th><th>控制字符</th>"
               "<th>十六进制</th><th>说明</th></tr></thead><tbody>%s</tbody></table></div>"
               % "".join("<tr><td class=\"mono\">%s</td><td class=\"mono\">%s</td>"
                         "<td class=\"mono\">%s</td><td>%s</td></tr>" % (esc(a), b, c, esc(d))
                         for a, b, c, d in esc_rows))

    # 扩展 ASCII 简表（Latin-1 常用）
    ext_rows = [
        ("0xA0", "160", "不换行空格 NBSP（HTML &amp;nbsp;）"),
        ("0xA9", "169", "版权符号 ©"),
        ("0xAE", "174", "注册商标 ®"),
        ("0xB0", "176", "度数符号 °"),
        ("0xB1", "177", "正负号 ±"),
        ("0xB5", "181", "微符号 µ"),
        ("0xB7", "183", "间隔号 ·"),
        ("0xD7", "215", "乘号 ×"),
        ("0xF7", "247", "除号 ÷"),
        ("0xFF", "255", "ÿ（Latin-1 最后一个码位）"),
    ]
    ext_tbl = ("<div class=\"scroll\"><table><thead><tr><th>十六进制</th><th>十进制</th>"
               "<th>说明</th></tr></thead><tbody>%s</tbody></table></div>"
               % "".join("<tr><td class=\"mono\">%s</td><td class=\"mono\">%s</td><td>%s</td></tr>"
                         % (a, b, c) for a, b, c in ext_rows))

    body = """
<section>
  <h2>控制字符 0–31<span class="en">Control characters</span></h2>
  <p class="sub">不可打印，在代码里以转义序列出现。日常真正会用到的其实只有 LF、CR、HT、NUL 四个。</p>
  %s
</section>

<section>
  <h2>可打印字符 32–126<span class="en">Printable characters</span></h2>
  <p class="sub">标准 ASCII 的可打印区间。注意 65–90 是大写字母，97–122 是小写字母，两者相差 32（0x20）。</p>
  %s
</section>

<section>
  <h2>常用转义对照<span class="en">Escape sequences</span></h2>
  <p class="sub">写代码、写正则、读日志时最常撞上的几个。</p>
  %s
  <div class="warn"><b>CRLF 是两个字节</b>文本里看到的「换行」在 Windows 上是 <code>\\r\\n</code>（0x0D 0x0A），在 Unix 上只有 <code>\\n</code>（0x0A）。跨平台处理文本时用 <code>bytes.replace(b"\\r\\n", b"\\n")</code> 统一，别用字符长度硬算。</div>
</section>

<section>
  <h2>DEL 与扩展区<span class="en">DEL and extended range</span></h2>
  <p>127（0x7F）是 <code>DEL</code>，历史上用于删除纸带上的一个字符。128–255 不属于标准 ASCII，属于 Latin-1（ISO-8859-1）等扩展字符集 —— 这段区间在中文字符编码里完全不同，不要混用。</p>
  %s
</section>

<section>
  <h2>容易踩的几个坑<span class="en">Gotchas</span></h2>
  <h3>1. 「127 个字符」是错的</h3>
  <p>标准 ASCII 是 0–127 共 <b>128</b> 个码位，其中 33 个控制字符 + 95 个可打印字符（含空格）。常说「128 个字符」才对。</p>
  <h3>2. 大小写差 32</h3>
  <p><code>'A' = 65</code>、<code>'a' = 97</code>，差 32。这个性质被大量用于位运算做大小写转换：<code>c | 0x20</code> 转小写，<code>c &amp; ~0x20</code> 转大写（仅对字母有效）。</p>
  <h3>3. 数字和字母不连续</h3>
  <p><code>'9' = 57</code> 之后是 <code>':' = 58</code>，不是 <code>'A'</code>。想判断字符是不是数字要用范围 <code>48–57</code>，不能靠「小于 A」。</p>
  <h3>4. 中文不属于 ASCII</h3>
  <p>任何中文字符都不是 ASCII，一个汉字在 UTF-8 下占 3 字节，在 GBK 下占 2 字节。看到「ASCII 乱码」基本都是编码不一致，而不是 ASCII 表用错。</p>
</section>
""" % (ctrl_tbl, print_tbl, esc_tbl, ext_tbl)

    return shell(
        "ascii",
        "ASCII 码表 · 0–127 完整对照（十进制/十六进制/字符/含义） | 开发者速查表",
        "ASCII 码表完整版：0–127 全部码位对照十进制、十六进制、字符与含义，含控制字符、常用转义序列、DEL 与扩展区说明。",
        body,
        "ASCII 码表",
        "ASCII Table · 0–127 with Decimal, Hex and Meaning",
        "0 到 127 全部码位，按控制字符与可打印字符分两块。手机上横向滑动可看完整列。",
        cta=("在线 ASCII 转换器", UTIL + "/ascii/"),
    )


# ---------------------------------------------------------------- HTTP 状态码
HTTP = [
    ("1xx", "信息响应", [
        (100, "Continue", "继续", "服务器已收到请求头，客户端应继续发送请求体。"),
        (101, "Switching Protocols", "切换协议", "响应 Upgrade 头，切换到 WebSocket 等协议。"),
        (102, "Processing", "处理中", "WebDAV，请求已收到但尚未完成。"),
        (103, "Early Hints", "早期提示", "在最终响应前先返回 Link 头，用于预加载资源。"),
    ]),
    ("2xx", "成功", [
        (200, "OK", "成功", "请求成功，响应体包含结果。"),
        (201, "Created", "已创建", "资源创建成功，通常配合 Location 头返回新资源地址。"),
        (202, "Accepted", "已接受", "请求已受理但尚未处理完，适合异步任务。"),
        (203, "Non-Authoritative Information", "非授权信息", "返回的是经过代理转换的元信息。"),
        (204, "No Content", "无内容", "成功但无响应体，常用于 DELETE、PUT。"),
        (205, "Reset Content", "重置内容", "要求客户端重置表单视图。"),
        (206, "Partial Content", "部分内容", "断点续传/分段下载，配合 Range 头使用。"),
        (207, "Multi-Status", "多状态", "WebDAV，响应体是 XML 描述多个子请求结果。"),
        (208, "Already Reported", "已报告", "WebDAV，避免重复枚举同一资源。"),
        (226, "IM Used", "IM 已使用", "Delta 编码，响应是实例操作的结果。"),
    ]),
    ("3xx", "重定向", [
        (300, "Multiple Choices", "多种选择", "资源有多个表示，需要客户端选择。"),
        (301, "Moved Permanently", "永久移动", "永久重定向，搜索引擎会传递权重并把索引切到新地址。"),
        (302, "Found", "临时移动", "临时重定向，历史实现可能把 POST 改成 GET。"),
        (303, "See Other", "查看其他", "明确要求客户端用 GET 访问 Location。"),
        (304, "Not Modified", "未修改", "协商缓存命中，响应无实体，直接用本地缓存。"),
        (305, "Use Proxy", "使用代理", "已废弃，客户端应通过代理访问。"),
        (307, "Temporary Redirect", "临时重定向", "临时跳转且<b>保持原方法</b>，POST 仍是 POST。"),
        (308, "Permanent Redirect", "永久重定向", "永久跳转且保持原方法，是 301 的方法安全版。"),
    ]),
    ("4xx", "客户端错误", [
        (400, "Bad Request", "请求错误", "语法错误、参数不合法，服务端无法解析。"),
        (401, "Unauthorized", "未认证", "缺少或无效的身份凭证 —— 先登录。"),
        (402, "Payment Required", "需要付费", "预留码，部分 API 用于表示额度耗尽。"),
        (403, "Forbidden", "禁止访问", "身份已识别但无权访问 —— 登录了也不给。"),
        (404, "Not Found", "未找到", "资源不存在。为避免泄露信息，也常用于掩盖 403。"),
        (405, "Method Not Allowed", "方法不允许", "接口存在但不支持该 HTTP 方法，响应带 Allow 头。"),
        (406, "Not Acceptable", "不可接受", "服务端无法提供客户端 Accept 头要求的格式。"),
        (407, "Proxy Authentication Required", "需要代理认证", "需先通过代理的身份验证。"),
        (408, "Request Timeout", "请求超时", "服务器等待请求完成超时。"),
        (409, "Conflict", "冲突", "请求与资源当前状态冲突，如并发写入、版本号不匹配。"),
        (410, "Gone", "已移除", "资源曾存在但已永久删除，搜索引擎应移除索引。"),
        (411, "Length Required", "需要长度", "缺少 Content-Length。"),
        (412, "Precondition Failed", "前置条件失败", "If-Match 等条件不成立，常见于乐观锁。"),
        (413, "Payload Too Large", "请求体过大", "超过服务端限制，需调整上传大小或 nginx client_max_body_size。"),
        (414, "URI Too Long", "URI 过长", "GET 参数塞太多，应改用 POST。"),
        (415, "Unsupported Media Type", "不支持的媒体类型", "Content-Type 不被接受，常见是漏了 application/json。"),
        (416, "Range Not Satisfiable", "范围不满足", "Range 头超出资源长度。"),
        (417, "Expectation Failed", "期望失败", "无法满足 Expect 请求头。"),
        (418, "I'm a teapot", "我是茶壶", "愚人节 RFC 2324，部分框架用它做彩蛋或拦截爬虫。"),
        (421, "Misdirected Request", "请求定向错误", "连接复用到不处理该域名的服务器，HTTP/2 常见。"),
        (422, "Unprocessable Entity", "无法处理的实体", "语法正确但语义校验失败，REST API 最常用它表示表单校验不通过。"),
        (423, "Locked", "已锁定", "WebDAV，资源被锁定。"),
        (424, "Failed Dependency", "依赖失败", "WebDAV，因前一个请求失败而失败。"),
        (425, "Too Early", "过早", "TLS 1.3 0-RTT 重放风险，服务端拒绝。"),
        (426, "Upgrade Required", "需要升级", "要求客户端升级协议，如强制 HTTPS 或 HTTP/2。"),
        (428, "Precondition Required", "需要前置条件", "要求请求带 If-Match 等条件，防止丢失更新。"),
        (429, "Too Many Requests", "请求过多", "触发限流，响应通常带 Retry-After。"),
        (431, "Request Header Fields Too Large", "请求头过大", "Cookie 或 header 太长，需精简。"),
        (451, "Unavailable For Legal Reasons", "因法律原因不可用", "因法律要求被屏蔽，如版权、合规审查。"),
    ]),
    ("5xx", "服务端错误", [
        (500, "Internal Server Error", "服务器内部错误", "未捕获异常，需要看服务端日志。"),
        (501, "Not Implemented", "未实现", "服务器不支持该请求方法。"),
        (502, "Bad Gateway", "网关错误", "网关从上游收到无效响应 —— 上游挂了或返回了垃圾。"),
        (503, "Service Unavailable", "服务不可用", "过载或维护中，通常带 Retry-After。"),
        (504, "Gateway Timeout", "网关超时", "网关等上游响应超时 —— 上游还活着但太慢。"),
        (505, "HTTP Version Not Supported", "HTTP 版本不支持", "不支持请求使用的 HTTP 版本。"),
        (506, "Variant Also Negotiates", "变体协商", "内容协商配置错误导致循环。"),
        (507, "Insufficient Storage", "存储不足", "WebDAV，服务器存储空间不足。"),
        (508, "Loop Detected", "检测到循环", "WebDAV，处理请求时出现无限循环。"),
        (510, "Not Extended", "未扩展", "需要进一步扩展请求才能处理。"),
        (511, "Network Authentication Required", "需要网络认证", "常见于公共 WiFi 门户认证拦截。"),
    ]),
]


def build_httpstatus():
    groups = []
    short = {
        "1xx": "1xx · 信息响应 Information",
        "2xx": "2xx · 成功 Success",
        "3xx": "3xx · 重定向 Redirection",
        "4xx": "4xx · 客户端错误 Client Error",
        "5xx": "5xx · 服务端错误 Server Error",
    }
    for code_cls, cn, items in HTTP:
        rows = "".join(
            "<tr><td class=\"mono\">%d</td><td class=\"mono\" style=\"color:var(--ink);font-weight:600\">%s</td>"
            "<td>%s</td><td>%s</td></tr>" % (c, esc(name), esc(cn), desc)
            for c, name, cn, desc in items
        )
        groups.append("""
<section>
  <h2>%s<span class="en">%s</span></h2>
  <div class="scroll"><table><thead><tr><th>码</th><th>标准名称</th><th>中文</th><th>说明</th></tr></thead>
  <tbody>%s</tbody></table></div>
</section>""" % (esc(short[code_cls]), esc(cn), rows))

    body = """
<section>
  <h2>先记住这四个<span class="en">The four that matter most</span></h2>
  <div class="scroll"><table><thead><tr><th>码</th><th>含义</th><th>一句话判断</th></tr></thead><tbody>
  <tr><td class="mono">200</td><td>成功</td><td>一切正常。</td></tr>
  <tr><td class="mono">301</td><td>永久重定向</td><td>地址换了，以后都去新地址。</td></tr>
  <tr><td class="mono">404</td><td>未找到</td><td>地址本身不对。</td></tr>
  <tr><td class="mono">500</td><td>服务器内部错误</td><td>地址对了，服务端自己崩了。</td></tr>
  </tbody></table></div>
  <p class="sub">排查顺序：先看状态码属于哪一类 —— 4xx 改客户端，5xx 看服务端日志，3xx 检查跳转链。</p>
</section>
%s

<section>
  <h2>最容易搞混的几组<span class="en">Confusing pairs</span></h2>

  <h3>401 还是 403？</h3>
  <p><b>401 Unauthorized</b>：你没证明你是谁 —— 没带 token、token 过期。正确做法是返回 <code>WWW-Authenticate</code> 头，引导重新认证。<br>
  <b>403 Forbidden</b>：服务器知道你是谁，但你没权限。此时重新登录也没用。<br>
  记忆法：401 = 没登录，403 = 登录了但不让进。</p>

  <h3>301 / 302 / 303 / 307 / 308 怎么选</h3>
  <div class="scroll"><table><thead><tr><th>码</th><th>是否永久</th><th>是否保持原方法</th><th>典型用途</th></tr></thead><tbody>
  <tr><td class="mono">301</td><td>永久</td><td>历史上常被改成 GET</td><td>域名迁移、http→https、去掉 www</td></tr>
  <tr><td class="mono">302</td><td>临时</td><td>历史上常被改成 GET</td><td>临时跳转、A/B 测试</td></tr>
  <tr><td class="mono">303</td><td>临时</td><td>强制改成 GET</td><td>POST 提交后跳转到结果页（PRG 模式）</td></tr>
  <tr><td class="mono">307</td><td>临时</td><td>保持</td><td>需要保住 POST body 的临时跳转</td></tr>
  <tr><td class="mono">308</td><td>永久</td><td>保持</td><td>需要保住 POST body 的永久跳转</td></tr>
  </tbody></table></div>
  <div class="tip"><b>一句话</b>表单 POST 想跳转就用 303；接口需要保方法用 307/308；普通页面迁移用 301。</div>

  <h3>502 还是 504？</h3>
  <p><b>502 Bad Gateway</b>：网关拿到了上游的<b>无效响应</b> —— 上游进程挂了、端口没监听、返回了非 HTTP 内容。<br>
  <b>504 Gateway Timeout</b>：网关<b>等不到</b>上游响应就超时了 —— 上游还活着，只是慢。<br>
  排查方向：502 查上游进程和端口（<code>ss -ltnp</code>、日志有没有启动失败）；504 查上游耗时（慢 SQL、下游依赖卡住）和网关超时配置（<code>proxy_read_timeout</code>）。</p>

  <h3>304 为什么没有响应体</h3>
  <p>304 是协商缓存命中：浏览器带着 <code>If-None-Match</code> / <code>If-Modified-Since</code> 来问，服务端说「没变，用你本地的」。所以响应必须没有 body，只有头。给 304 塞 body 会导致部分客户端解析异常。</p>

  <h3>418 能用在生产吗</h3>
  <p>能 —— 它是一个合法注册的状态码，很多站点用它拦截特定爬虫（返回 418 而不是 403，避免被当成权限错误）。但别用它表示正常的业务失败。</p>
</section>

<section>
  <h2>状态码分类速记<span class="en">Class semantics</span></h2>
  <ul>
    <li><b>1xx</b>：还在协商，不是最终结果。</li>
    <li><b>2xx</b>：成功。注意 204 没有 body，别在里面读 JSON。</li>
    <li><b>3xx</b>：需要再走一步。客户端要能跟随跳转，但 API 调用通常应关闭自动跟随以便观测。</li>
    <li><b>4xx</b>：客户端的问题。同一个请求重发不会有不同结果，别做无脑重试。</li>
    <li><b>5xx</b>：服务端的问题。可重试，但要带退避，否则放大故障。</li>
  </ul>
</section>
""" % "".join(groups)

    return shell(
        "httpstatus",
        "HTTP 状态码速查 · 1xx–5xx 全量中文对照 | 开发者速查表",
        "HTTP 状态码完整速查表：1xx 到 5xx 全量状态码中文含义与说明，含 401/403、301/302/303/307/308、502/504 等易混辨析与排查方向。",
        body,
        "HTTP 状态码速查",
        "HTTP Status Codes · 1xx to 5xx Reference",
        "全量状态码中文对照，外加最容易搞混的几组（401/403、502/504、3xx 全家）该怎么选。",
        cta=("状态码排查工具", UTIL + "/httpstatus/"),
    )


# ---------------------------------------------------------------- Cron
CRON_FIELDS = [
    ("分钟", "minute", "0–59", "*", "每小时的第几分钟"),
    ("小时", "hour", "0–23", "*", "每天的第几小时"),
    ("日", "day of month", "1–31", "*", "每月的第几天"),
    ("月", "month", "1–12 或 JAN–DEC", "*", "第几个月"),
    ("星期", "day of week", "0–7 或 SUN–SAT", "*", "0 和 7 都表示周日"),
]

CRON_SYMBOLS = [
    ("<code>*</code>", "任意值", "该字段所有可能值都匹配。<code>* * * * *</code> 是每分钟。"),
    ("<code>,</code>", "枚举", "<code>1,15,30</code> 表示 1、15、30 三个值。"),
    ("<code>-</code>", "范围", "<code>9-17</code> 表示 9 到 17，含两端。"),
    ("<code>/</code>", "步长", "<code>*/5</code> 每 5 个单位，<code>10-50/10</code> 表示 10 到 50 每 10 个。"),
    ("<code>?</code>", "不指定", "仅 Quartz 方言支持，表示「不关心」该字段，不能与 <code>*</code> 混用在同一字段。"),
    ("<code>L</code>", "最后", "Quartz：<code>L</code> 在日字段表示当月最后一天，在星期字段表示最后一个周几。"),
    ("<code>W</code>", "工作日", "Quartz：<code>15W</code> 表示离 15 号最近的工作日。"),
    ("<code>#</code>", "第几个", "Quartz：<code>5#2</code> 表示当月第二个周五。"),
]

CRON_EXAMPLES = [
    ("* * * * *", "每分钟执行"),
    ("*/5 * * * *", "每 5 分钟"),
    ("0 * * * *", "每小时整点"),
    ("0 */2 * * *", "每 2 小时整点"),
    ("30 3 * * *", "每天 03:30"),
    ("0 0 * * *", "每天 00:00"),
    ("0 9 * * 1-5", "周一到周五 09:00"),
    ("0 9 * * MON-FRI", "同上，用英文缩写写法"),
    ("0 0 * * 0", "每周日 00:00"),
    ("0 0 1 * *", "每月 1 号 00:00"),
    ("0 0 1 */3 *", "每季度首日 00:00（1、4、7、10 月）"),
    ("0 0 1 1 *", "每年 1 月 1 日 00:00"),
    ("0 2 * * 6", "每周六 02:00"),
    ("*/10 9-18 * * 1-5", "工作日 9–18 点之间每 10 分钟"),
    ("0 8,12,18 * * *", "每天 8 点、12 点、18 点"),
    ("15 14 1 * *", "每月 1 号 14:15"),
    ("0 22 * * 1-5", "工作日 22:00"),
    ("23 0-23/2 * * *", "每 2 小时的第 23 分钟（00:23、02:23…）"),
    ("5 4 * * SUN", "每周日 04:05"),
    ("0 0,12 1 */2 *", "每隔一个月的 1 号，0 点和 12 点各一次"),
    ("0 4 8-14 * *", "每月 8–14 号每天 04:00"),
    ("0 0 1,15 * 3", "每月 1 号和 15 号，且仅当是周三 —— 见下方陷阱"),
]

CRON_MACROS = [
    ("@yearly / @annually", "0 0 1 1 *", "每年 1 月 1 日 00:00"),
    ("@monthly", "0 0 1 * *", "每月 1 日 00:00"),
    ("@weekly", "0 0 * * 0", "每周日 00:00"),
    ("@daily / @midnight", "0 0 * * *", "每天 00:00"),
    ("@hourly", "0 * * * *", "每小时整点"),
    ("@reboot", "—", "系统启动时运行一次（不适用于在线 Cron 服务）"),
]


def build_cron():
    fields_rows = "".join(
        "<tr><td class=\"mono\">%s</td><td>%s</td><td class=\"mono\" style=\"color:var(--ink)\">%s</td><td>%s</td></tr>"
        % (esc(cn), esc(en), esc(rng), esc(note))
        for cn, en, rng, _, note in CRON_FIELDS
    )
    sym_rows = "".join(
        "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (sym, esc(name), note)
        for sym, name, note in CRON_SYMBOLS
    )
    ex_rows = "".join(
        "<tr><td class=\"mono\">%s</td><td>%s</td></tr>" % (esc(expr), esc(desc))
        for expr, desc in CRON_EXAMPLES
    )
    macro_rows = "".join(
        "<tr><td class=\"mono\">%s</td><td class=\"mono\" style=\"color:var(--ink)\">%s</td><td>%s</td></tr>"
        % (esc(a), esc(b), esc(c)) for a, b, c in CRON_MACROS
    )
    field_head = "<th>字段</th><th>Field</th><th>取值范围</th><th>说明</th>"

    body = """
<section>
  <h2>五字段结构<span class="en">The five fields</span></h2>
  <p class="sub">标准 cron 表达式由 5 个空白分隔的字段组成，从左到右依次是：</p>
  <div class="scroll"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>
  <div class="tip"><b>容易记反</b>顺序是<b>分 时 日 月 周</b>，不是「年月日时分」。<code>30 2 * * *</code> 是「每天 2:30」，不是「2 点 30 分」写反。</div>
</section>

<section>
  <h2>特殊符号<span class="en">Special characters</span></h2>
  <div class="scroll"><table><thead><tr><th>符号</th><th>含义</th><th>用法</th></tr></thead><tbody>%s</tbody></table></div>
  <div class="warn"><b>方言警告</b><code>?</code>、<code>L</code>、<code>W</code>、<code>#</code> 是 <b>Quartz（Java 系）</b>的扩展语法，标准 Vixie Cron 和大多数 Linux crontab <b>不支持</b>。写进 crontab 会直接报错。用之前先确认你的调度器是哪一种。</div>
</section>

<section>
  <h2>常用写法<span class="en">Common patterns</span></h2>
  <p class="sub">直接抄这一栏基本够用。</p>
  <div class="scroll"><table><thead><tr><th>表达式</th><th>含义</th></tr></thead><tbody>%s</tbody></table></div>
</section>

<section>
  <h2>快捷宏<span class="en">Macros</span></h2>
  <div class="scroll"><table><thead><tr><th>宏</th><th>等价表达式</th><th>含义</th></tr></thead><tbody>%s</tbody></table></div>
  <p class="sub">宏只有部分实现支持。crontab 里可以用，但很多在线 Cron 服务不支持 <code>@reboot</code>。</p>
</section>

<section>
  <h2>四个经典陷阱<span class="en">Gotchas</span></h2>

  <h3>1. 日和星期同时指定，是「或」不是「与」</h3>
  <p>这是最反直觉的一点。当<b>日</b>和<b>星期</b>两个字段都不是 <code>*</code> 时，Vixie Cron 的语义是<b>满足任意一个就触发</b>，而不是两个都满足。</p>
  <p>例：<code>0 0 1,15 * 3</code> 的本意可能是「每月 1 号和 15 号，且必须是周三」，但实际含义是「每月 1 号、15 号<b>或者</b>每个周三」—— 触发次数远超预期。</p>
  <div class="warn"><b>怎么绕过</b>想让两个条件同时成立，只能在脚本内部加判断（比如检查 <code>date +%%u</code> 是否为 3），或者改用支持 <code>?</code> 的 Quartz 方言。</div>

  <h3>2. 星期从 0 还是 1 开始</h3>
  <p>Vixie Cron 里 <b>0 和 7 都表示周日</b>，1 是周一。但 Quartz 里 1 是周日，7 是周六。跨系统迁移 cron 表达式时，这里最容易静默出错 —— 不会报错，只是执行时间整体偏移一天。用英文缩写 <code>SUN</code>–<code>SAT</code> 可以避开这个坑。</p>

  <h3>3. 时区不是你以为的那个</h3>
  <p>crontab 的时区跟随<b>系统时区</b>（<code>/etc/timezone</code> 或 <code>TZ</code> 环境变量），不是用户所在时区。服务器常是 UTC，于是「每天 09:00」实际是北京时间 17:00。</p>
  <p>容器里更要注意：镜像默认 UTC，即使宿主机是 CST。</p>

  <h3>4. 分钟步长不会「对齐到整点」</h3>
  <p><code>*/7 * * * *</code> 不是每 7 分钟均匀跑一次，而是在 0、7、14…56 分跑，然后下一小时又从 0 开始 —— 56 到下一个 0 之间只隔 4 分钟。步长不能整除 60 时，边界处间隔会不均匀。</p>
  <p>需要严格等间隔，就用秒级调度器（systemd timer、K8s CronJob 之外的方案）或让脚本自己 sleep。</p>
</section>

<section>
  <h2>写完之后一定要验算<span class="en">Verify before you deploy</span></h2>
  <p>cron 表达式最坑的地方是：写错了不会报错，只会安静地在该跑的时候不跑，或者不该跑的时候疯狂跑。上线前至少做两件事：</p>
  <ol>
    <li>用解析器把表达式翻译成「未来 5 次执行时间」，肉眼对一遍。</li>
    <li>确认调度器的时区，并把时区差异折算成实际本地时间。</li>
  </ol>
  <p>本页只解决「怎么写」，算不出「下次什么时候跑」—— 那需要真正的解析器。用下面的工具直接看未来执行时间。</p>
</section>
""" % (field_head, fields_rows, sym_rows, ex_rows, macro_rows)

    return shell(
        "cron",
        "Cron 表达式速查 · 语法、符号、常用示例与陷阱 | 开发者速查表",
        "Cron 表达式中文速查：5 字段含义、* , - / ? L W # 特殊符号用法、20+ 常用写法、@daily 等快捷宏，以及日与星期「或」语义等四个经典陷阱。",
        body,
        "Cron 表达式速查",
        "Cron Expression Reference · Syntax, Symbols & Examples",
        "五个字段怎么排、特殊符号什么含义、常用写法直接抄，外加四个不会报错但会让你半夜排查的陷阱。",
        cta=("在线 Cron 解析器（看下次执行时间）", UTIL + "/cron/"),
    )


# ---------------------------------------------------------------- 其他文件
ROBOTS = """User-agent: *
Allow: /

Sitemap: %s/sitemap.xml
""" % BASE_URL

# IndexNow（Bing / Yandex 即时收录）key 文件，与 maqiangthunder.github.io 上其他项目站点共用同一 key
INDEXNOW_KEY = "93ea49b44c5ab1387d572caf5c00ed1a"

# 搜索引擎站长验证
# Bing：根文件放项目子路径下 Bing 未必认（它按站点根校验），所以同时用 meta 标签验证
BING_MSVALIDATE = "3064BAE72021AEE71FDF47842243FED1"
BING_AUTH = """<?xml version="1.0"?>
<users>
\t<user>%s</user>
</users>
""" % BING_MSVALIDATE
GOOGLE_VERIFY_FILE = "google31716acc6e0ed1fd.html"
GOOGLE_VERIFY_CONTENT = "google-site-verification: google31716acc6e0ed1fd.html\n"

SITEMAP = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
%s
</urlset>
"""

README = """# 开发者速查表 · Developer Cheat Sheets

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
"""

LICENSE = """MIT License

Copyright (c) 2026 maqiangThunder

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


def write(path, content):
    full = os.path.join(OUT, path)
    d = os.path.dirname(full)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote %s (%d bytes)" % (full, len(content.encode("utf-8"))))


def main():
    os.makedirs(OUT, exist_ok=True)
    write("index.html", build_index())
    write("ascii/index.html", build_ascii())
    write("httpstatus/index.html", build_httpstatus())
    write("cron/index.html", build_cron())
    write("robots.txt", ROBOTS)
    write(".nojekyll", "")
    write(INDEXNOW_KEY + ".txt", INDEXNOW_KEY)
    write("BingSiteAuth.xml", BING_AUTH)
    write(GOOGLE_VERIFY_FILE, GOOGLE_VERIFY_CONTENT)

    # sitemap
    urls = [("", "1.0"), ("ascii/", "0.9"), ("httpstatus/", "0.9"), ("cron/", "0.9")]
    items = []
    for slug, pri in urls:
        loc = BASE_URL + "/" + slug
        items.append(
            "  <url>\n    <loc>%s</loc>\n    <lastmod>2026-11-09</lastmod>\n"
            "    <changefreq>monthly</changefreq>\n    <priority>%s</priority>\n  </url>" % (loc, pri)
        )
    write("sitemap.xml", SITEMAP % "\n".join(items))


if __name__ == "__main__":
    main()
