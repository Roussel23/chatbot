from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
# from django.utils.translation import   

# Cette partie permet de generer un token
class AppTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (force_str(user.is_active) + force_str(user.pk) + force_str(timestamp))


account_activation_token = AppTokenGenerator()

