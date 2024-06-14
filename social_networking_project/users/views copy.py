from django.contrib.auth import get_user_model, authenticate
from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, LoginSerializer
from .serializers import UserSearchSerializer
from drf_yasg.utils import swagger_auto_schema


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        # Check if the email and password are provided
        if not email or not password:
            return Response({"detail": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user based on email
        user = User.objects.filter(email=email).first()
        if user is not None and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
from rest_framework.permissions import IsAuthenticated

class PrintHelloWorldView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return None  # or any dummy serializer you want

    def get(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            return Response({"message": "Hello, World!"})
        else:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

class UserSearchAPIView(generics.ListAPIView):
    serializer_class = UserSerializer  # Use the appropriate serializer for User details

    def get_queryset(self):
        search_keyword = self.request.query_params.get('search_keyword', '')
        if search_keyword:
            # Filter users where either email or username contains the search keyword
            queryset = User.objects.filter(email__icontains=search_keyword) | \
                       User.objects.filter(username__icontains=search_keyword)
        else:
            queryset = User.objects.none()  # Return empty queryset if no search keyword provided
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)