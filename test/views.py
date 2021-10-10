from django.shortcuts import render 
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList
from .forms import CreateNewList

# Create your views here.

def index(request, id):
    ls = ToDoList.objects.get(id=id)
    if not ls in request.user.todolist_set.all(): 
        return HttpResponse('err')



    print (request.POST)
    if request.method == 'POST':
        print ('saving')
        if request.POST.get('save'):
            print ('has')
            for item in ls.item_set.all():
                if request.POST.get('c' + str(item.id) ):
                    item.complete = True
                else:
                    item.complete = False
                item.save()
             


        elif request.POST.get('newItem'):
            print ('newi')
            txt = request.POST.get('new')
            if len(txt) > 2:
                ls.item_set.create(text=txt, complete=False)
            else: print ('err')
            ls.save()
    


    return render(request, 'list.html', {'ls': ls})

def home(request):
    return render(request, 'home.html', {})

def create(request):
    u = request.user 
    if request.method == 'POST':
        form = CreateNewList(request.POST)
        if form.is_valid():
            n = form.cleaned_data['name']
            t = u.todolist_set.create(name = n)
            u.save()
            return HttpResponseRedirect('/%i' % t.id)

    else:
        form= CreateNewList()
    return render(request, 'create.html', {'form': form})

