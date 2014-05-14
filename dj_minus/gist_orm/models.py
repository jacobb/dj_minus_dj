import json

from django.contrib.auth.models import AbstractUser
from django.db import models

import requests

from .secret import FOAUTH_EMAIL, FOAUTH_PASS

GITHUB_API = "https://foauth.org/api.github.com/"
FOAUTH_AUTH = (FOAUTH_EMAIL, FOAUTH_PASS)


class GistUser(AbstractUser):

    gist_id = models.CharField(max_length=255, unique=True)

    DEFAULT_PASSWORD = 'default'
    _JSON = None

    def serialize(self):

        user_dict = {
            'description': self.username,
            'files': {
                'password.txt': {
                    'content': self.gist_password
                }
            }
        }

        return user_dict

    def set_password(self, password):
        """
        Who needs hashing, LOL
        """
        serialized = self.serialize()

        serialized['files']['password.txt']['content'] = password
        url = "%sgists/%s" % (GITHUB_API, self.gist_id)
        res = requests.patch(url, auth=FOAUTH_AUTH, data=json.dumps(serialized))

        print res
        if res.status_code != 200:
            raise ValueError("Something Went wrong")

    @property
    def gist_password(self):
        if not self._JSON:
            return self.DEFAULT_PASSWORD

        password_file = self._JSON['files'].get('password.txt')

        if not password_file:
            return self.DEFAULT_PASSWORD

        return password_file['content']
