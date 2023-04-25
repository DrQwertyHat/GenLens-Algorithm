from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework import viewsets, permissions
from .serializers import UserSerializer
from .forms import UserProfileForm
from .models import UserProfile

User = get_user_model()

class AccountViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save()


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        token = self._get_token(user)

        return Response({'token': token})

    def _get_token(self, user):
        serializer = VerifyJSONWebTokenSerializer(data={'token': user.token})
        serializer.is_valid(raise_exception=True)

        return serializer.validated_data['token']


def create_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile_detail')
    else:
        form = UserProfileForm()
    return render(request, 'core/create_profile.html', {'form': form})
    
def profile_detail(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'core/profile_detail.html', {'profile': profile})