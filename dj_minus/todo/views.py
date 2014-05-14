from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import RequestContext

from jinja_env import env

# Create your views here.


def jinja_render(request, template_name, dictionary=None):

    if not dictionary:
        dictionary = {}
    template = env.get_template("index.html")
    new_context = RequestContext(request, dictionary)
    context_dict = {}
    for d in new_context.dicts:
        context_dict.update(d)

    rendered_template = template.render(**context_dict)
    return HttpResponse(rendered_template)


@login_required
def home(request):

    # return render(request, "index.html")
    return jinja_render(request, "index.html")


def login(request):
    pass


def logout_view(request):
    logout(request)

    url = "/"
    return HttpResponseRedirect(url)
