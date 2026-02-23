import json

# بارگذاری داده‌های کانفیگ از فایل
with open('config.json', 'r') as file:
    configs = json.load(file)

# اعمال تغییرات (اضافه کردن پیشوند "Mine" به هر کانفیگ)
modified_configs = []
for i, config in enumerate(configs):
    config['name'] = f"Mine{i+1}_{config['name']}"
    modified_configs.append(config)

# ذخیره فایل تغییر یافته
with open('modified_config.json', 'w') as file:
    json.dump(modified_configs, file, indent=4)
