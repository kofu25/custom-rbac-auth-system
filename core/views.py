from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from .models import User, AccessRule, UserRole, Role
from .services import check_password, create_token, has_permission, hash_password
from .serializers import UserRegisterSerializer, UserUpdateSerializer, AccessRuleSerializer

class RegisterView(APIView):
    authentication_classes = [] # Пусто для регистрации
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create(
                full_name=serializer.validated_data['full_name'],
                email=serializer.validated_data['email'],
                password_hash=hash_password(serializer.validated_data['password_hash'])
            )
            user_role, _ = Role.objects.get_or_create(name='User')
            UserRole.objects.create(user=user, role=user_role)
            return Response({"message": "User created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    authentication_classes = [] # Пусто для логина
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            # Ищем только активных
            user = User.objects.get(email=email, is_active=True)
            if check_password(password, user.password_hash):
                token = create_token(user.id)
                return Response({'token': token})
        except User.DoesNotExist:
            pass
        return Response({'error': 'Invalid credentials'}, status=401)

class LogoutView(APIView):
    def post(self, request):
        return Response({"message": "Successfully logged out"}, status=200)

class UserProfileView(APIView):
    def get(self, request):
        if not request.user: 
            return Response({"error": "Unauthorized"}, status=401)
        return Response({'full_name': request.user.full_name, 'email': request.user.email})

    def patch(self, request):
        if not request.user: 
            return Response({"error": "Unauthorized"}, status=401)
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request):
        if not request.user: 
            return Response({"error": "Unauthorized"}, status=401)
        request.user.is_active = False
        request.user.save()
        return Response({'message': 'Account deactivated'})

class AccessRuleViewSet(viewsets.ModelViewSet):
    queryset = AccessRule.objects.all()
    serializer_class = AccessRuleSerializer

    def list(self, request, *args, **kwargs):
        if not has_permission(request.user, 'ACCESS_RULE', 'read'):
            return Response({"error": "Forbidden"}, status=403)
        return super().list(request, *args, **kwargs)

class ProductMockView(APIView):
    def get(self, request):
        if not request.user: 
            return Response({"error": "Unauthorized"}, status=401)
        if not has_permission(request.user, 'PRODUCT', 'read'):
            return Response({'error': 'Forbidden'}, status=403)
        return Response([{'id': 1, 'name': 'Laptop'}])