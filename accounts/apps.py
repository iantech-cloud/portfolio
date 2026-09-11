from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        from django.db.models.signals import post_save
        from .models import create_profile
        post_save.connect(create_profile, sender="accounts.User", dispatch_uid="accounts.create_profile")
