from django.shortcuts import render,redirect
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User,Role
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
import logging
from .forms import UserRegistrationForm
logger = logging.getLogger(__name__)


class UserListView(APIView):
    def get(self,request):

        user = User.objects.all()
        serializer_class = UserSerializer(user,many=True)
        return Response(serializer_class.data,status=status.HTTP_200_OK)

    def post(self, request):
        post_serialzer=UserSerializer(data=request.data)
        if post_serialzer.is_valid():
            post_serialzer.save()
            return Response(post_serialzer.data,status=status.HTTP_201_CREATED)
        return Response(post_serialzer.errors)
    
class UserUpdateView(APIView): 
    def get_user(self,username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404
    def get(self,request,username):

        user = self.get_user(username)
        serializer = UserSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self, request, username): 
        user = self.get_user(username)
        serializer = UserSerializer(user, data=request.data, partial=True) 
        if serializer.is_valid(): 
            roles = request.data.get('roles',[]) 
            if roles: 
                role_instances = [] 
                for role_name in roles: 
                    role, created = Role.objects.get_or_create(role=role_name) 
                    if created:
                        print(f"created new role :{role_name}")
                    role_instances.append(role) 
                for role in role_instances:
                    if role not in user.roles.all():
                        user.roles.add(role)    
                
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {"error": "Please provide both username and password"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Authenticate user
        logger.info(f"Trying to authenticate username: {username}")
        user = authenticate(username=username, password=password)
        if user is not None:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                status=status.HTTP_200_OK
            )
        else:
            logger.warning(f"Authentication failed for username: {username}")
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )    
        
class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "username": user.username,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "email": user.email,
            "roles": [role.role for role in user.roles.all()],
        }
        return Response(data, status=status.HTTP_200_OK)        


def add_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')  # Replace with your desired redirection URL
    else:
        form = UserRegistrationForm()
    return render(request, 'add_user.html', {'form': form})