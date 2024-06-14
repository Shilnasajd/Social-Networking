from django.contrib.auth import get_user_model, authenticate
from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, LoginSerializer, RegisterSerializer
from .serializers import UserSearchPagination, FriendRequestSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import FriendRequest
from rest_framework import permissions, throttling
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from .pagination import CustomPagination

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
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
    
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

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
    pagination_class = CustomPagination

    def get_queryset(self):
        search_keyword = self.request.query_params.get('search_keyword', '')
        if search_keyword:
            queryset = User.objects.filter(email__icontains=search_keyword) | \
                       User.objects.filter(username__icontains=search_keyword)
        else:
            queryset = User.objects.none()  # Return empty queryset if no search keyword provided
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
            
class FriendRequestThrottle(throttling.UserRateThrottle):
    rate = '3/min'

class SendFriendRequestAPIView(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [FriendRequestThrottle]  # Add the throttle class

    def perform_create(self, serializer):
        # Get the authenticated user from the request
        from_user = self.request.user

        # Get the "to_user" ID from the request data
        to_user_id = self.request.data.get('to_user')

        # Check if the "to_user" ID is provided
        if not to_user_id:
            raise ValidationError('The "to_user" field is required.')

        # Check if the "to_user" is the same as the "from_user"
        if from_user.id == int(to_user_id):
            raise ValidationError('You cannot send a friend request to yourself.')

        # Get the "to_user" instance
        to_user = User.objects.filter(id=to_user_id).first()

        # Check if the "to_user" exists
        if not to_user:
            raise ValidationError('Invalid "to_user" ID.')

        # Check if a friend request has already been sent
        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            raise ValidationError('Friend request already sent.')

        # Save the friend request with the authenticated user as the sender
        serializer.save(from_user=from_user, to_user=to_user)

        # Optionally return a success response
        return Response({'detail': 'Friend request sent successfully.'})
        
        
class AcceptRejectFriendRequestAPIView(generics.UpdateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        request_id = request.data.get('id')
        if request_id is None:
            return Response({'detail': 'Request ID is required in the request body.'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the friend request instance
        try:
            instance = FriendRequest.objects.get(id=request_id)
        except FriendRequest.DoesNotExist:
            return Response({'detail': 'Friend request not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the authenticated user is the recipient of the friend request
        if instance.to_user != request.user:
            return Response({'detail': 'You are not authorized to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        # Update the accepted status based on the request data
        accepted = request.data.get('accepted', None)
        if accepted is None:
            return Response({'detail': 'Accepted field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        instance.accepted = accepted
        instance.save()

        # Optionally return a success response
        return Response({'status': 'Friend request updated'}, status=status.HTTP_200_OK)
    

class ListFriendsAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        from_user_ids = FriendRequest.objects.filter(to_user=self.request.user, accepted=True).values_list('from_user', flat=True)
        to_user_ids = FriendRequest.objects.filter(from_user=self.request.user, accepted=True).values_list('to_user', flat=True)
        friend_ids = set(from_user_ids) | set(to_user_ids)
        return User.objects.filter(id__in=friend_ids)
    

class ListPendingFriendRequestsAPIView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only allow listing pending friend requests where the authenticated user is the sender
        return FriendRequest.objects.filter(to_user=self.request.user, accepted=False)