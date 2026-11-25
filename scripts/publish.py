#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AsanWay Instagram Publisher — فقط با کتابخانه استاندارد پایتون.
هر اجرا یک آیتم از content.json را (به‌ترتیب چرخشی) منتشر می‌کند.

Secrets لازم (GitHub Secrets):
  IG_ACCESS_TOKEN : توکن طولانی‌عمر Graph API
  IG_USER_ID      : شناسه اکانت اینستاگرام بیزینس

اگر سکرت‌ها تنظیم نشده باشند، اسکریپت با پیام راهنما خارج می‌شود (بدون کرش).
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content.json")
STATE = os.path.join(ROOT, "state", "state.json")
RAW_BASE = "https://raw.githubusercontent.com/atasana/asanway-ig/main"

TOKEN = os.environ.get("IG_ACCESS_TOKEN", "").strip()
USER = os.environ.get("IG_USER_ID", "").strip()
GRAPH = "https://graph.facebook.com/v21.0"


def summary(text):
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(text.rstrip() + "\n\n")
    print(text, flush=True)


def graph(path, params, method="GET"):
    url = "{}/{}/{}".format(GRAPH, USER, path)
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(url, data=data if method == "POST" else None, method=method)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode())


def load_state():
    try:
        with open(STATE, encoding="utf-8") as fh:
            return json.load(fh).get("next", 0)
    except Exception:
        return 0


def save_state(next_index):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    with open(STATE, "w", encoding="utf-8") as fh:
        json.dump({"next": next_index}, fh)


def main():
    if not TOKEN or not USER:
        summary(
            "سکرت‌های اینستاگرام تنظیم نشده است.\n\n"
            "Settings ← Secrets and variables ← Actions:\n"
            "- IG_ACCESS_TOKEN (توکن Graph API)\n"
            "- IG_USER_ID (شناسه اکانت بیزینس)\n\n"
            "راهنمای کامل در README-fa.md مخزن است."
        )
        sys.exit(0)

    with open(CONTENT, encoding="utf-8") as fh:
        items = json.load(fh)
    index = load_state() % len(items)
    item = items[index]
    media_url = "{}/{}".format(RAW_BASE, item["asset"])
    caption = item["caption"]

    if item["type"] == "image":
        created = graph("{}/media".format(USER), {
            "access_token": TOKEN, "image_url": media_url, "caption": caption
        }, "POST")
    else:
        created = graph("{}/media".format(USER), {
            "access_token": TOKEN, "media_type": "REELS",
            "video_url": media_url, "caption": caption,
        }, "POST")
        creation_id = created.get("id")
        if not creation_id:
            summary("خطا: پاسخ ساخت مدیا بدون شناسه.")
            sys.exit(1)
        for _ in range(60):
            status = graph(creation_id, {"access_token": TOKEN, "fields": "status_code"})
            code = status.get("status_code")
            if code == "FINISHED":
                break
            if code == "ERROR":
                summary("پردازش ویدیو در اینستاگرام خطا داد.")
                sys.exit(1)
            time.sleep(10)
        else:
            summary("پردازش ویدیو بیش از ۱۰ دقیقه طول کشید؛ اجرای بعدی تلاش می‌کند.")
            sys.exit(1)
        created = {"id": creation_id}

    creation_id = created.get("id")
    published = graph("{}/media_publish".format(USER), {
        "access_token": TOKEN, "creation_id": creation_id
    }, "POST")
    post_id = published.get("id")
    save_state(index + 1)
    summary(
        "منتشر شد: آیتم {} از {} — {} (post id: {})".format(
            index + 1, len(items), item["asset"], post_id
        )
    )


if __name__ == "__main__":
    main()
