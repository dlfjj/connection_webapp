from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views import generic
from .models import *
import connectionsGrabber
import os

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('query')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


class ConnectionsView(generic.ListView):
    template_name = 'IntroManager/querydisplay.html'
    context_object_name = 'prims_list'
    
    def post(self, request, *args, **kwargs):
        inputurl = request.POST.get('searchinput')
        un = request.POST.get('username')
        pw = request.POST.get('password')
        currentobj = Seconds.objects.filter(url=inputurl) # try to find curr obj in db
        if not currentobj: # if no matching obj found in DB
            currentobj = scrapeURLandAddToDB(inputurl,un,pw) # scrape connection info and add curr obj info to DBs
        else:
            currentobj = currentobj[0]
        prims_list = findMutualConnectionsToInputURL(inputurl)
        return render(request, self.template_name, 
        	{
        		'prims_list': prims_list,
        		'searched': currentobj.name
        	})

    # def post2(self, request, *args, **kwargs):
    #     inputurl = request.POST.get('searchinput')
    #     currentobj = Seconds.objects.filter(url=inputurl) # try to find curr obj in db
    #     if not currentobj: # if no matching obj found in DB
    #         scrapeURLandAddToDB(inputurl) # scrape connection info and add curr obj info to DBs
    #     prims_list = findMutualConnectionsToInputURL(inputurl)
    #     return render(request, self.template_name, 
    #         {
    #             'prims_list': prims_list,
    #             'searched': currentobj
    #         })
   
    def get_queryset(self):
        return Seconds.objects.all()

def findMutualConnectionsToInputURL(inputURL):
    # get a list of Primary conns corresponding to the input URL of the second deg conn
    currentqueryobjs = Seconds.objects.filter(url=inputURL)   # get the current object
    currobj_uid = currentqueryobjs[0].uid   # get the current object's UID
    connslist = Conns.objects.filter(id2=currobj_uid)   # search conns to find all the primary's connected to current obj
    connectedid1s = getValuesFromQueryObjs(connslist, 'id1')
    primarieslist = list(Prims.objects.filter(uid__in = connectedid1s).order_by('-numShared')) # get all the primary's connected to current obj
    return primarieslist

def getValuesFromQueryObjs(queryobjs,field):
    # get a list of values corresponding to a certain field in each obj in the query
    objvalslist = queryobjs.values(field)
    output = [ obj[field] for obj in objvalslist ]
    return output

def scrapeURLandAddToDB(inputurl,un,pw):
    datalist,searchedperson = connectionsGrabber.main(un, pw, inputurl)
    s,junk = Seconds.objects.get_or_create(
        name=searchedperson['name'],
        url=searchedperson['url'],
        title=searchedperson['title'],
        location=searchedperson['location'],
                                           #numShared=searchedperson['numShared']
        )
    for data in datalist: 
        # 'data' has fields defined in the output of connectionsGrabber 
        # (those names were chosen to match the model's field names)
        try:
            p,junk = Prims.objects.get_or_create(
                        name=data['name'],
                        title=data['title'],
                        location=data['location'],
                                                 #numShared=data['numShared'],
                        url=data['url']
                )
            c = Conns.objects.create(
                id1 = p,
                id2 = s
                )
        except:
            print "you got error"
    return s
