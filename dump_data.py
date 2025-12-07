import os
import django
from django.core.management import call_command

# Установите переменную окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProjects')

# Настройка Django
django.setup()

# Теперь можно использовать call_command
with open('groups.json', 'w', encoding='utf-8') as f:
    call_command('dumpdata', 'auth', output=f)