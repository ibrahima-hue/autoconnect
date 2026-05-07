from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .serializers import RegisterSerializer, LoginSerializer, TokenResponseSerializer, UserSerializer
from .models import User, PlatformSettings


@api_view(['GET'])
@permission_classes([AllowAny])
def public_settings(request):
    cfg = PlatformSettings.get()
    return Response({'premium_enabled': cfg.premium_enabled})


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(TokenResponseSerializer.get_tokens(user), status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = (request.data.get('email') or '').lower().strip()
    try:
        u = User.objects.get(email__iexact=email)
        if u.is_banned:
            return Response({
                'account_status': 'banned',
                'reason': u.ban_reason or '',
                'ban_until': u.ban_until.isoformat() if u.ban_until else None,
            }, status=status.HTTP_403_FORBIDDEN)
        if not u.is_active:
            return Response({
                'account_status': 'suspended',
                'reason': u.ban_reason or '',
                'ban_until': u.ban_until.isoformat() if u.ban_until else None,
            }, status=status.HTTP_403_FORBIDDEN)
    except User.DoesNotExist:
        pass

    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        return Response(TokenResponseSerializer.get_tokens(user))
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Deconnexion : on essaie de blacklister le refresh token si possible.
    Ne bloque jamais : meme sans blacklist, le client supprime ses tokens."""
    refresh = request.data.get('refresh')
    if refresh:
        try:
            RefreshToken(refresh).blacklist()
        except (TokenError, AttributeError):
            # Blacklist app non installee ou token invalide : on ignore
            pass
    return Response({'detail': 'Deconnexion reussie.'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    return Response(UserSerializer(request.user).data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_avatar(request):
    file = request.FILES.get('avatar')
    if not file:
        return Response({'error': 'Aucun fichier fourni.'}, status=status.HTTP_400_BAD_REQUEST)
    user = request.user
    if user.avatar_image:
        user.avatar_image.delete(save=False)
    user.avatar_image = file
    user.save()
    return Response(UserSerializer(user, context={'request': request}).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    old_password = request.data.get('old_password', '')
    new_password = request.data.get('new_password', '')

    if not user.check_password(old_password):
        return Response({'error': 'Mot de passe actuel incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
    if len(new_password) < 6:
        return Response({'error': 'Le nouveau mot de passe doit contenir au moins 6 caractères.'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()
    return Response({'detail': 'Mot de passe modifié avec succès.'})
