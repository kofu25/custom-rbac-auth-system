import jwt
import bcrypt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework import authentication
from .models import User, UserRole, AccessRule

# --- КЛАСС АУТЕНТИФИКАЦИИ ДЛЯ DRF ---
class CustomJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'], is_active=True)
            return (user, token)
        except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
            return None

    def authenticate_header(self, request):
        return 'Bearer'

# --- ТВОИ ФУНКЦИИ ---
def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password: str, hashed: str):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def create_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

def has_permission(user, object_name, action, owner_id=None):
    if not isinstance(user, User):
        return False
    
    user_roles = UserRole.objects.filter(user=user).values_list('role_id', flat=True)
    rules = AccessRule.objects.filter(role_id__in=user_roles, business_object__name=object_name)
    
    for rule in rules:
        if action == 'create' and rule.can_create: return True
        if action == 'read' and rule.can_read_all: return True
        if action == 'update' and rule.can_update_all: return True
        if action == 'delete' and rule.can_delete_all: return True
        if owner_id and user.id == owner_id:
            if action == 'read' and rule.can_read_own: return True
            if action == 'update' and rule.can_update_own: return True
            if action == 'delete' and rule.can_delete_own: return True
    return False