from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf

from core.forms import EntryForm
from core.models import Entry

hello_world = TemplateView.as_view(template_name='hello-world.html')
def index(request):
    # List the title and created date of all posts. (maybe paginated, maybe include first paragraph)
    entries = Entry.all()
    return render_to_response('index.html', {'entries': entries})
    
def add_entry(request):
    
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            instance = Entry(title=data['title'], content=data['content'])
            instance.put()
        return HttpResponseRedirect("/entry/%s" % instance.key().id())
    else:
        form = EntryForm()
        c = {'form': form}
        c.update(csrf(request))
        return render_to_response('edit.html', c)

def edit_entry(request, entry_id):

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
        c = {'form': form}
        c.update(csrf(request))
        return render_to_response('edit.html', c)
    
def entry(request, entry_id):
    entry = Entry.get_by_id(long(entry_id))
    return render_to_response('entry.html', {'entry': entry})