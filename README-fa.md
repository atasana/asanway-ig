# آسان‌وی — انتشار خودکار اینستاگرام

این مخزن پست‌ها و ریلزهای صفحه اینستاگرام **asanway.co** را کاملاً خودکار منتشر می‌کند:
هر روز ساعت **۱۲:۰۰** یک پست (تصویر یا ریلز) با کپشن فارسی، هشتگ و دعوت به واتس‌اپ.

- ۹ پست تصویری (برف‌پاکن آیسین، لنت ادویکس، شمع NGK)
- ۳ ریلز ۱۵ ثانیه‌ای ۱۰۸۰×۱۹۲۰
- چرخش خودکار ۱۲ آیتم؛ ترتیب در فایل `state/state.json` ذخیره می‌شود

## راه‌اندازی (یک‌بار)

۱. اکانت اینستاگرام باید **Professional (Business یا Creator)** باشد:
   Instagram ← Settings ← Account type and tools ← Switch to professional account

۲. یک **صفحه فیسبوک** بسازید (یا دارید) و اکانت اینستاگرام را به آن وصل کنید:
   Instagram ← Edit profile ← Page ← Connect

۳. در [developers.facebook.com](https://developers.facebook.com) یک **App** از نوع Business بسازید و
   Product به نام **Instagram Graph API** را اضافه کنید. اکانت شما نقش Admin/Developer همان اپ است،
   پس بدون نیاز به بررسی (Review) می‌توانید برای اکانت خودتان منتشر کنید.

۴. توکن بسازید: Graph API Explorer ← Generate Access Token با مجوزهای
   `instagram_basic`, `instagram_content_publish`, `pages_show_list`, `business_management`
   سپس با Exchange به توکن ۶۰ روزه و بعد به **توکن طولانی‌عمر** تبدیل کنید.

۵. در همین مخزن: Settings ← Secrets and variables ← Actions ← دو سکرت:
   - `IG_ACCESS_TOKEN`
   - `IG_USER_ID` (شناسه عددی اکانت اینستاگرام — از `/me?fields=accounts` در Graph API Explorer)

۶. در تب Actions گردش‌کار `AsanWay Instagram Publisher` را یک‌بار با حالت `test` اجرا کنید،
   سپس حالت `publish` — اولین پست منتشر می‌شود.

## ساختار

```
assets/feed/    ۹ تصویر پست (۱۰۸۰×۱۳۵۰)
assets/reels/   ۳ ریلز (۱۰۸۰×۱۹۲۰، ۱۵ ثانیه)
content.json    صف انتشار با کپشن‌ها
scripts/        publish.py — انتشار با Graph API (بدون کتابخانه اضافه)
state/          نشانگر چرخش
```

## آدرس‌دهی رسانه‌ها

فایل‌ها از آدرس عمومی زیر به سرورهای اینستاگرام معرفی می‌شوند:
`https://raw.githubusercontent.com/atasana/asanway-ig/main/<asset>`

## افزودن محتوای تازه

۱. تصویر جدید را در `assets/feed/` بگذارید (۱۰۸۰×۱۳۵۰) یا ویدیو در `assets/reels/` (۱۰۸۰×۱۹۲۰، زیر ۱ دقیقه).
۲. یک آیتم به `content.json` اضافه کنید: type برای تصویر `image` و برای ویدیو `reels`.
۳. Commit کنید — در چرخش روزانه خودش منتشر می‌شود.
