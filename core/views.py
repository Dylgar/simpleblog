from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse

from google.appengine.api import users

from core.forms import EntryForm
from core.models import Entry

import logging

def is_user_admin(func):
    def wrapper(request, *args, **kwargs):
        user = users.get_current_user()
        if user and users.is_current_user_admin():
            return func(request, *args, **kwargs)
        return HttpResponseRedirect(reverse(index))
        
    return wrapper

def _get_default_template_data(request):
    user = users.get_current_user()
    login_url = users.create_login_url(request.path)
    logout_url = users.create_logout_url(request.path)
    data = {'user': user,
            'login_url': login_url,
            'logout_url': logout_url}
    return data
    
def index(request):
    # List the title and created date of all posts. (maybe paginated, maybe include first paragraph)
    # Add sorting by created date
    entries = Entry.all()
    data = _get_default_template_data(request)
    data['entries'] = entries
    return render_to_response('index.html', data)

@is_user_admin
def add_entry(request):
    data = _get_default_template_data(request)
    if not data['user']:
        return HttpResponseRedirect(users.create_login_url(request.path))
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            instance = Entry(title=data['title'], 
                             content=data['content'], 
                             labels=data['labels'].split(' '))
            instance.put()
        return HttpResponseRedirect("/entry/%s" % instance.key().id())
    else:
        form = EntryForm()
        data['form'] = form
        data.update(csrf(request))
        return render_to_response('edit.html', data)

@is_user_admin
def edit_entry(request, entry_id):
    data = _get_default_template_data(request)
    if not data['user']:
        return HttpResponseRedirect(users.create_login_url(request.path))
    entry = Entry.get_by_id(long(entry_id))
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            entry.title = form.cleaned_data['title']
            entry.content = form.cleaned_data['content']
            entry.put()
            return HttpResponseRedirect("/entry/%s/" % entry_id)
    else:
        form = EntryForm(initial={'title': entry.title, 'content': entry.content})
        data['form'] = form
        data.update(csrf(request))
        return render_to_response('edit.html', data)
    
def entry(request, entry_id):
    data = _get_default_template_data(request)
    data['user_is_admin'] = users.is_current_user_admin()
    data['entry'] = Entry.get_by_id(long(entry_id))
    return render_to_response('entry.html', data)