import os
import requests
import base64
import json
from datetime import datetime

SOURCE_FILE = "sources/subs.txt"
OUTPUT_DIR = "output"

# تابع خواندن ساب لینک‌ها از فایل
def read_sources():
    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

# تابع دریافت کانفیگ از لینک
def fetch_sub(url):
    try:
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            return r.text.strip()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return None

# تابع دیکد کردن محتوا در صورت Base64 بودن
def decode_if_base64(content):
    try:
        decoded = base64.b64decode(content).decode("utf-8")
        if "://" in decoded:
            return decoded
    except:
        pass
    return content

# تابع تبدیل به فرمت ویلس
def convert_to_wills(content):
    return f"wills_config = {content}"

# تابع تبدیل به فرمت تروجان
def convert_to_trojan(content):
    return f"trojan_config = {content}"

# تابع ذخیره کردن فایل با نام شمارنده
def save_output(content, counter):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    filename = f"Mine{counter:02d}.conf"  # تغییر نام به Mine01, Mine02, ...
    file_path = os.path.join(OUTPUT_DIR, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

# عملیات اصلی
def main():
    sources = read_sources()

    # پردازش کانفیگ‌ها
    for i, url in enumerate(sources, start=1):
        print(f"Fetching {url}")
        data = fetch_sub(url)
        if data:
            data = decode_if_base64(data)

            # فرض می‌کنیم که داده‌ها به فرمت JSON هستند
            try:
                json_data = json.loads(data)
                # تبدیل به فرمت‌های مختلف (ویلس و تروجان)
                wills_config = convert_to_wills(json.dumps(json_data, indent=4))
                trojan_config = convert_to_trojan(json.dumps(json_data, indent=4))

                # ذخیره خروجی
                save_output(wills_config, i)
                save_output(trojan_config, i)

            except json.JSONDecodeError:
                print(f"Invalid JSON for {url}")
                continue

if __name__ == "__main__":
    main()
