from django.contrib.auth.models import User
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        if sociallogin.is_existing:
            return

        if 'email' not in sociallogin.account.extra_data:
            return

        try:
            email = sociallogin.account.extra_data['email'].lower()
            print(email)
            email_address = User.objects.get(email=email)
            print(email_address)
        except:
            return

        user = email_address
        user.first_name = sociallogin.account.extra_data['given_name']
        user.save()
        sociallogin.connect(request, user)