#!/usr/bin/env python3
"""sitemap.xml 產生器。新增語系或可索引頁面時重跑：

    python3 scripts/build-sitemap.py

只收錄「有內容可索引」的頁面：五語首頁、五語教學頁、法務頁。
/account 與 /recover 是工具頁（登入後才有東西），交給 robots.txt 擋。
"""

import datetime
import pathlib

SITE = "https://soma-agent.com"
NS = "http://www.sitemaps.org/schemas/sitemap/0.9"  # sitemaps，不是 sitemap
LANGS = [("", "zh-Hant"), ("cn", "zh-Hans"), ("en", "en"), ("ja", "ja"), ("ko", "ko")]
PAGES = [("", "1.0", "weekly"), ("help", "0.8", "monthly")]

ROOT = pathlib.Path(__file__).resolve().parent.parent
today = datetime.date.today().isoformat()


def alternates(page: str) -> str:
    rows = [
        f'    <xhtml:link rel="alternate" hreflang="{code}" '
        f'href="{SITE}/{d + "/" if d else ""}{page}"/>'
        for d, code in LANGS
    ]
    rows.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}/en/{page}"/>')
    return "\n".join(rows)


def main() -> None:
    urls = []
    for page, prio, freq in PAGES:
        for d, _ in LANGS:
            urls.append(
                f"""  <url>
    <loc>{SITE}/{d + "/" if d else ""}{page}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{prio}</priority>
{alternates(page)}
  </url>"""
            )
    urls.append(
        f"""  <url>
    <loc>{SITE}/legal.html</loc>
    <lastmod>{today}</lastmod>
    <changefreq>yearly</changefreq>
    <priority>0.3</priority>
  </url>"""
    )

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        "<!-- 由 scripts/build-sitemap.py 產生，不要手改 -->\n"
        f'<urlset xmlns="{NS}"\n        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")
    print(f"sitemap.xml：{xml.count('<url>')} 筆")


if __name__ == "__main__":
    main()
