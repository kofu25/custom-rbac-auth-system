import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_auth_system.settings')
django.setup()

from core.models import Role, BusinessObject, AccessRule, User, UserRole
from core.services import hash_password

def run():
    print("Инициализация базы данных...")
    
    # 1. Роли
    admin_role, _ = Role.objects.get_or_create(name='Admin')
    user_role, _ = Role.objects.get_or_create(name='User')

    # 2. Объекты
    obj_product, _ = BusinessObject.objects.get_or_create(name='PRODUCT')
    obj_profile, _ = BusinessObject.objects.get_or_create(name='USER_PROFILE')
    obj_rules, _ = BusinessObject.objects.get_or_create(name='ACCESS_RULE')

    # 3. Правила для Админа (используем update_or_create)
    for obj in [obj_product, obj_profile, obj_rules]:
        AccessRule.objects.update_or_create(
            role=admin_role, business_object=obj,
            defaults={
                'can_create': True, 
                'can_read_all': True, 
                'can_update_all': True, 
                'can_delete_all': True
            }
        )

    # 4. Тестовый Админ
    admin_user, created = User.objects.get_or_create(
        email='admin@test.com',
        defaults={
            'full_name': 'Главный Админ',
            'password_hash': hash_password('admin123'),
            'is_active': True
        }
    )
    # Если админ уже был, но неактивен - активируем
    if not created:
        admin_user.is_active = True
        admin_user.save()

    UserRole.objects.get_or_create(user=admin_user, role=admin_role)
    
    print("Готово! База данных настроена.")

if __name__ == '__main__':
    run()