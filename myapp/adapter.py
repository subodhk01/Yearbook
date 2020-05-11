from django.contrib.auth.models import User
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter

class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        print(request.user)
        return False

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        if sociallogin.is_existing:
            return

        if 'email' not in sociallogin.account.extra_data:
            return

        try:
            email = sociallogin.account.extra_data['email'].strip().lower()
            print(email)
            user_object = User.objects.get(email=email)
            print(user_object)
        except:
            return

        user = user_object
        if not user.first_name:
            user.first_name = sociallogin.account.extra_data.get('given_name', '')
        user.last_name = sociallogin.account.extra_data.get('family_name','')
        user.save()
        sociallogin.connect(request, user)