#!/usr/bin/env python3
"""يولّد موقعاً ثابتاً: صفحة HTML حقيقية لكل منشور + sitemap.xml + robots.txt.
التشغيل:  python3 build.py   ثم ارفع مجلد dist إلى Cloudflare Pages."""
import os, json, shutil, html
from datetime import date
SITE_URL = "https://YOUR-SITE.pages.dev"   # <-- غيّره إلى رابط موقعك الحقيقي ثم أعد البناء
SITE_NAME = "المنصة القانونية اليمنية"
TAGLINE = "منصة لكل ما هو متعلق بالقانون"
SECTIONS = [
 ("laws","التشريعات اليمنية","نصوص القوانين والتشريعات اليمنية"),
 ("regs","اللوائح","اللوائح التنفيذية والتنظيمية"),
 ("contracts","صيغ العقود","نماذج وصيغ عقود ومذكرات"),
 ("research","الأبحاث القانونية","أبحاث ودراسات قانونية"),
 ("rulings","أحكام المحكمة العليا","مبادئ وأحكام المحكمة العليا"),
]
ICON = {"laws": "⚖️", "regs": "📁"}
HOME_CARDS = [
 ("/legislation/","⚖️","التشريعات واللوائح","تصفح القسم",False),
 ("/contracts/","📜","صيغ العقود","تصفح القسم",False),
 ("/research/","📚","الأبحاث القانونية","تصفح القسم",False),
 ("/rulings/","📌","أحكام المحكمة العليا","تصفح القسم",False),
 ("https://judg.moj.gov.ye:8065/Identity/Account/Login?ReturnUrl=%2F","💻","الدعاوى الإلكترونية","دخول البوابة",True),
 ("https://judg.moj.gov.ye/JUDDATALIST/CustomRetCaseMaster","🔍","البحث عن القضايا","دخول البوابة",True),
]
SOCIAL_LINKS = [("فيسبوك","https://www.facebook.com/Jabrsalehlaw/"),("تيك توك","https://www.tiktok.com/@jabrsalehlaw"),("يوتيوب","https://www.youtube.com/@jabrsalehlaw"),("انستقرام","https://www.instagram.com/jabrsalehlaw"),("تلجرام","https://t.me/Jabrsalehlaw"),("واتساب","https://whatsapp.com/channel/0029VabIj5pKgsNxObIy050i")]
ST = {s[0]: s[1] for s in SECTIONS}
e = html.escape
def write(path, txt):
    p = os.path.join("dist", path.lstrip("/"))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(txt)
def parse(path):
    head, blocks, inbody = {}, [], False
    for ln in open(path, encoding="utf-8").read().splitlines():
        ln = ln.strip()
        if not inbody:
            if ln == "---": inbody = True
            elif ":" in ln: k, v = ln.split(":", 1); head[k.strip()] = v.strip()
        elif ln.startswith("## "): blocks.append(("h", ln[3:]))
        elif ln.startswith("@ ") and "|" in ln:
            n, t = ln[2:].split("|", 1); blocks.append(("a", n.strip(), t.strip()))
        elif ln: blocks.append(("p", ln))
    return head, blocks
SITE_EMAIL = "info@example.com"   # <-- بريد التواصل
LOGO = '<svg viewBox="0 0 32 32" width="30" height="30" aria-hidden="true"><path d="M16 6v19M9 25h14M7 11h18M7 11l-3 8h6zM25 11l-3 8h6z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
PAGES = {
 "about": ("من نحن", ["المنصة القانونية اليمنية مكتبة عربية مجانية تجمع التشريعات والأحكام القضائية وصيغ العقود والأبحاث والشروحات في مكان واحد، وتقدمها بلغة واضحة وتصنيف منظم يسهّل البحث.", "هدفنا تقريب المعرفة القانونية من الجميع. ندرج المصدر كلما أمكن، ونراجع المنشورات ونحدّثها عند تغيّر النصوص.", "المحتوى معرفي عام، وليس استشارة قانونية."]),
 "contact": ("اتصل بنا", ["يسعدنا استقبال اقتراحاتكم وتصحيحاتكم، أو طلب إضافة قانون أو نموذج.", "راسلنا على البريد: " + SITE_EMAIL]),
 "privacy": ("سياسة الخصوصية", ["لا يطلب الموقع منك تسجيل حساب، ولا يجمع بياناتك الشخصية ولا يستخدم ملفات تعريف الارتباط (كوكيز) بنفسه.", "يحمّل الموقع الخطوط من Google Fonts، وقد تسجّل Google وCloudflare بيانات تقنية عامة مثل عنوان IP بحسب سياساتهما.", "عند مشاركة منشور عبر واتساب أو تلجرام فأنت تنتقل إلى خدماتهم وتخضع لسياساتهم."]),
 "disclaimer": ("إخلاء المسؤولية", ["المحتوى المنشور للتثقيف والمعلومات العامة ولا يُعد استشارة قانونية ولا يقوم مقامها.", "قد تتغير القوانين وتُعدَّل، فارجع دائماً إلى النص الرسمي المعمول به، واستشر محامياً مختصاً في قضيتك قبل اتخاذ أي إجراء."]),
}
def cardlinks():
    return "".join(f'<a href="{u}"' + (' target="_blank" rel="noopener"' if x else "") + f'>{e(t)}</a>' for u, _, t, _, x in HOME_CARDS)
def social():
    return "".join(f'<a href="{u}" target="_blank" rel="noopener">{e(n)}</a>' for n, u in SOCIAL_LINKS)
def layout(title, desc, url, main, ld=None, noindex=False):
    full = title if url == "/" else f"{title} | {SITE_NAME}"
    sl = cardlinks()
    pl = "".join(f'<a href="/{k}/">{e(v[0])}</a>' for k, v in PAGES.items())
    nav = cardlinks()
    ldt = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False).replace("</","<\\/")}</script>' if ld else ""
    robots = '<meta name="robots" content="noindex">' if noindex else ""
    return f'''<!DOCTYPE html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full)}</title><meta name="description" content="{e(desc)}">{robots}
<link rel="canonical" href="{SITE_URL}{url}"><link rel="icon" href="/favicon.png" type="image/png"><link rel="apple-touch-icon" href="/favicon.png"><meta name="theme-color" content="#0E4D4A">
<meta property="og:type" content="website"><meta property="og:locale" content="ar_AR"><meta property="og:site_name" content="{e(SITE_NAME)}">
<meta property="og:title" content="{e(full)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{SITE_URL}{url}"><meta property="og:image" content="{SITE_URL}/og.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Cairo:wght@400;600;700&display=swap">
<link rel="stylesheet" href="/style.css">{ldt}<script src="/site.js" defer></script></head>
<body><a class="skip" href="#main">تخطي إلى المحتوى</a>
<header class="top"><div class="wrap"><a class="brand" href="/"><img src="/logo.png" alt="شعار {e(SITE_NAME)}" width="70" height="66">{e(SITE_NAME)}</a><nav class="nav" aria-label="الأقسام">{nav}</nav>
<form class="search" action="/search/" method="get" role="search"><input id="q" name="q" type="search" aria-label="ابحث في المنصة" placeholder="بحث" required><button type="submit">بحث</button></form></div></header>
<main id="main">{main}</main>
<footer class="foot"><div class="wrap"><div class="fcols"><div><h2>{e(SITE_NAME)}</h2><p>{e(TAGLINE)}</p></div><div><h2>الأقسام</h2>{sl}</div><div><h2>المنصة</h2>{pl}</div><div><h2>تابعنا</h2>{social()}</div></div>
<small>المحتوى للتثقيف والمعرفة العامة ولا يغني عن استشارة محامٍ مختص في قضيتك. <br>جميع الحقوق محفوظة لدى © (جبر صالح جبر) {e(SITE_NAME)} {date.today().year}</small></div></footer></body></html>'''
def W(x): return f'<div class="wrap">{x}</div>'
def li(it):
    return f'<div class="li"><h3><a href="{it["url"]}">{e(it["title"])}</a></h3><p>{e(it["desc"])}</p><a class="tag" href="/{it["sec"]}/">{e(ST[it["sec"]])}</a></div>'
items = []
for sid, _, _ in SECTIONS:
    d = os.path.join("content", sid)
    if not os.path.isdir(d): continue
    for f in sorted(os.listdir(d)):
        if not f.endswith(".txt"): continue
        h, b = parse(os.path.join(d, f)); slug = f[:-4]
        first = next((x[1] for x in b if x[0] == "p"), next((x[2] for x in b if x[0] == "a"), h.get("title", "")))
        items.append(dict(sec=sid, slug=slug, url=f"/{sid}/{slug}/", title=h.get("title", slug), date=h.get("date", str(date.today())), blocks=b, desc=first[:155]))
shutil.rmtree("dist", ignore_errors=True)
shutil.copytree("static", "dist")
items.sort(key=lambda i: i["date"], reverse=True)
# الرئيسية
cnt = {sid: sum(1 for i in items if i["sec"] == sid) for sid, _, _ in SECTIONS}
chips = cardlinks()
idx = ""
for u, ic, t, lab, x in HOME_CARDS:
    at = ' target="_blank" rel="noopener"' if x else ""
    idx += f'<a href="{u}"{at}><span class="ic" aria-hidden="true">{ic}</span><strong>{e(t)}</strong><em>{lab}</em></a>'
hero = (f'<section class="hero"><div class="wrap"><h1>كل ما تحتاجه في القانون، في مكان واحد</h1><p>{e(TAGLINE)}</p>'
        f'<form class="hs" action="/search/" method="get" role="search"><input name="q" type="search" aria-label="ابحث في المنصة" placeholder="ابحث عن قانون أو مادة أو مصطلح" required><button type="submit">بحث</button></form>'
        f'<div class="chips">{chips}</div></div></section>')
write("/index.html", layout(SITE_NAME, TAGLINE, "/",
  hero + W(f'<h2 class="sec">أقسام المنصة الرئيسية</h2><div class="index">{idx}</div><h2 class="sec">أحدث المنشورات</h2>{"".join(li(i) for i in items[:10])}'),
  ld={"@context": "https://schema.org", "@type": "WebSite", "name": SITE_NAME, "url": SITE_URL, "inLanguage": "ar", "sameAs": [u for _, u in SOCIAL_LINKS]}))
# الأقسام
for sid, t, d in SECTIONS:
    its = [i for i in items if i["sec"] == sid]
    body = "".join(li(i) for i in its) or '<p class="empty">لا توجد منشورات في هذا القسم بعد.</p>'
    write(f"/{sid}/index.html", layout(t, d, f"/{sid}/", W(f'<h2 class="sec">{e(t)}</h2><p class="empty" style="padding-top:0">{e(d)}</p>{body}')))
hub = "".join(f'<a href="/{i}/"><span class="ic" aria-hidden="true">{ICON[i]}</span><strong>{e(t)}</strong><em>{cnt[i]} منشور</em></a>' for i, t, _ in SECTIONS if i in ICON)
write("/legislation/index.html", layout("التشريعات واللوائح", "التشريعات اليمنية واللوائح", "/legislation/", W(f'<h2 class="sec">التشريعات واللوائح</h2><div class="index">{hub}</div>')))
# صفحات المنصة
for k, (t, ps) in PAGES.items():
    write(f"/{k}/index.html", layout(t, ps[0][:155], f"/{k}/", W(f'<article class="article" style="margin-top:32px"><h1>{e(t)}</h1><div class="body">{"".join("<p>"+e(x)+"</p>" for x in ps)}</div></article>')))
# المنشورات
for it in items:
    rows, toc, n = "", "", 0
    for b in it["blocks"]:
        if b[0] == "h":
            n += 1; rows += f'<h2 id="h{n}">{e(b[1])}</h2>'; toc += f'<li><a href="#h{n}">{e(b[1])}</a></li>'
        elif b[0] == "a": rows += f'<div class="art"><b>{e(b[1])}</b><span>{e(b[2])}</span></div>'
        else: rows += f"<p>{e(b[1])}</p>"
    words = sum(len(" ".join(b[1:]).split()) for b in it["blocks"]); mins = max(1, round(words / 180))
    rel = "".join(li(r) for r in [x for x in items if x["sec"] == it["sec"] and x is not it][:5])
    relh = f'<section class="related"><h2>منشورات ذات صلة</h2>{rel}</section>' if rel else ""
    tocb = f'<div class="box"><h2>في هذا المنشور</h2><ol>{toc}</ol></div>' if toc else ""
    secs = cardlinks()
    u = SITE_URL + it["url"]
    main = W(f'<nav class="crumb"><a href="/">الرئيسية</a> &gt; {'<a href="/legislation/">التشريعات واللوائح</a> &gt; ' if it["sec"] in ICON else ""}<a href="/{it["sec"]}/">{e(ST[it["sec"]])}</a></nav>'
        f'<div class="cols"><article class="article"><h1>{e(it["title"])}</h1><div class="meta"><span>آخر تحديث: {it["date"]}</span><span>وقت القراءة: {mins} دقائق</span></div>'
        f'<div class="body">{rows}</div><div class="tools"><button type="button" data-print>طباعة / حفظ PDF</button>'
        f'<a href="https://wa.me/?text={u}" rel="noopener" target="_blank">واتساب</a><a href="https://t.me/share/url?url={u}" rel="noopener" target="_blank">تلجرام</a></div></article>'
        f'<aside class="side">{tocb}<div class="box"><h2>الأقسام</h2>{secs}</div></aside></div>{relh}')
    write(it["url"] + "index.html", layout(it["title"], it["desc"], it["url"], main, ld=[
      {"@context": "https://schema.org", "@type": "Article", "headline": it["title"], "datePublished": it["date"], "dateModified": it["date"], "inLanguage": "ar", "mainEntityOfPage": u, "publisher": {"@type": "Organization", "name": SITE_NAME}},
      {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": SITE_NAME, "item": SITE_URL + "/"},
        {"@type": "ListItem", "position": 2, "name": ST[it["sec"]], "item": f"{SITE_URL}/{it['sec']}/"},
        {"@type": "ListItem", "position": 3, "name": it["title"], "item": u}]}]))
# البحث وملفات الفهرسة
write("/search/index.html", layout("بحث", "البحث في المنصة", "/search/", W('<h2 class="sec" id="qtitle">ابحث في المنصة</h2><div id="results"></div>'), noindex=True))
write("/404.html", layout("الصفحة غير موجودة", "الصفحة غير موجودة", "/404/", W('<h2 class="sec">الصفحة غير موجودة</h2><p class="empty"><a href="/">العودة للرئيسية</a></p>'), noindex=True))
json.dump([dict(t=i["title"], u=i["url"], s=ST[i["sec"]], x=" ".join(" ".join(b[1:]) for b in i["blocks"])) for i in items],
          open("dist/search.json", "w", encoding="utf-8"), ensure_ascii=False)
urls = [("/", str(date.today())), ("/legislation/", str(date.today()))] + [(f"/{s}/", str(date.today())) for s, _, _ in SECTIONS] + [(f"/{k}/", str(date.today())) for k in PAGES] + [(i["url"], i["date"]) for i in items]
write("/sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
      "".join(f"<url><loc>{SITE_URL}{u}</loc><lastmod>{d}</lastmod></url>" for u, d in urls) + "</urlset>")
write("/robots.txt", f"User-agent: *\nAllow: /\nDisallow: /search/\nSitemap: {SITE_URL}/sitemap.xml\n")
print(f"تم: {len(items)} منشور، {len(urls)} رابط في الخريطة")
