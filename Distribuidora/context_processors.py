from .models import Avatar

def user_avatar(request):
    user = request.user
    avatar = None  # Valor predeterminado si el usuario no tiene un avatar
    
    if user.is_authenticated:
        avatar = Avatar.objects.filter(user=user).first()

    return {
        'user_avatar': avatar,
    }