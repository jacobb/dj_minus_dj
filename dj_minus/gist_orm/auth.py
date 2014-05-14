import requests

# hidden from by gitignore, add your own!
from .models import GistUser, GITHUB_API
from .secret import FOAUTH_EMAIL, FOAUTH_PASS


FOAUTH_AUTH = (FOAUTH_EMAIL, FOAUTH_PASS)


class SuperInsecureGistAuthBackend(object):

    def get_user(self, user_id):
        try:
            u = GistUser.objects.get(id=user_id)
        except GistUser.DoesNotExist:
            u = None

        return u

    def authenticate(self, **credentials):
        username = credentials['username']
        password = credentials['password']

        user_gists = self.get_gists()

        if username not in user_gists:
            return None

        user_dict = self.get_user_data(user_gists[username])
        real_password = user_dict['files']['password.txt']['content']

        if password == real_password:
            user, created = GistUser.objects.get_or_create(username=username)
            if created:
                user.gist_id = user_dict['id']
                user.save()

            user._JSON = user_dict

            return user

    def get_user_data(self, github_url):
        user_file_url = github_url.replace("https://", "https://foauth.org/")
        user_file_res = requests.get(user_file_url, auth=FOAUTH_AUTH)

        return user_file_res.json()

    def get_gists(self):

        suffix = "gists"
        users_url = "%s%s" % (GITHUB_API, suffix)
        res = requests.get(users_url, auth=FOAUTH_AUTH)
        users = dict([
            (g['description'], g['url'])
            for g in res.json()
            if 'password.txt' in g['files']
        ])
        return users
