# export_data.py

import os
import json
import django
from django.core import serializers
from django.apps import apps

# 1. Укажите путь к настройкам проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# 2. Инициализируйте Django
django.setup()

# 3. Теперь можно безопасно получать модели
Permission = apps.get_model('auth', 'Permission')
Group = apps.get_model('auth', 'Group')

# 4. Сериализуйте данные
data = []
for model in [Permission, Group]:
    data.extend(json.loads(serializers.serialize('json', model.objects.all())))

# 5. Сохраните в файл с кодировкой UTF-8
with open('groups.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)