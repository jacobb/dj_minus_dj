from .models import GistUser


class AuthRoulette(object):
    """
    So I can F5 until I'm Frank
    """

    def process_request(self, request):
        u = GistUser.objects.order_by('?')[0]

        if request.user:
            request.user = u
