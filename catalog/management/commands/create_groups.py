from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission
from catalog.models import Product


class Command(BaseCommand):
    help = 'Creates moderator and content manager groups with permissions'

    def handle(self, *args, **options):
        # Группа модераторов продуктов
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')

        # Получаем разрешения
        unpublish_perm = Permission.objects.get(codename='can_unpublish_product')
        change_status_perm = Permission.objects.get(codename='can_change_product_status')
        delete_product_perm = Permission.objects.get(codename='delete_product')

        # Назначаем разрешения группе
        moderator_group.permissions.add(unpublish_perm, change_status_perm, delete_product_perm)

        self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" создана с нужными правами'))

        # Дополнительно: Группа контент-менеджеров (для дополнительного задания)
        content_manager_group, created = Group.objects.get_or_create(name='Контент-менеджер')
        blog_perms = Permission.objects.filter(
            codename__in=['add_blogpost', 'change_blogpost', 'delete_blogpost']
        )
        content_manager_group.permissions.add(*blog_perms)

        self.stdout.write(self.style.SUCCESS('Группа "Контент-менеджер" создана с нужными правами'))
