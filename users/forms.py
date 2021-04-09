from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'username', 'email')

    def clean(self):
        for key in self.data.keys():
            if 'username' in key:
                user_exists = User.objects.filter(
                    username=self.data[key]).exists()
                if self.data[key] in settings.FORBIDDEN_USERNAMES or \
                        user_exists:
                    self.add_error('username',
                                   'К сожалению, это имя нельзя использовать')
