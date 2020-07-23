from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown
import random

from . import util
from . import views

class EntryForm(forms.Form):
    pageName = forms.CharField(label="Title")
    pageContent = forms.CharField(label="Content")

class editPageForm(forms.Form):
    pageName = forms.CharField(label="Title")
    pageContent = forms.CharField(label="Content")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,entryname):
    content = util.get_entry(entryname)
    markdowner = Markdown()
    contentConverted = markdowner.convert(content)
    if content == None:
        errorM = "Requested page could not be found"
        return render(request,"encyclopedia/error.html",{
            "ErrorMessage" : errorM
        }) #sends error page
    else:
        return render(request,"encyclopedia/entry.html",{
            "entrytitle" : entryname,
            "content" : contentConverted,
        })

def search(request):
    keyword = request.GET['q']
    searchResult, matchFound = util.search_entry(keyword)

    if len(searchResult) > 0:
        resultPresent = True
    else:
        resultPresent = False
    if matchFound:
        #Redirect to specific page
        foundEntry = searchResult[0]
        return HttpResponseRedirect(reverse('entry', args=[foundEntry]))
    else:
        #how search results
        return render(request, "encyclopedia/search.html",{
            "SearchResults": searchResult,
            "resultFound": resultPresent
        })

def createPage(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["pageName"]
            content = form.cleaned_data["pageContent"]
            if util.get_entry(title):
                errorM = "Page already exists. Can't create new page."
                return render(request,"encyclopedia/error.html",{
                    "ErrorMessage" : errorM
                })
            else:
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse('entry', args=[title]))
        else:
            errorM = "Invalid Form"
            return render(request,"encyclopedia/error.html",{
                "ErrorMessage" : errorM
            })
    return render(request,"encyclopedia/createPage.html")

def entryEdit(request,entryname):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["pageName"]
            content = form.cleaned_data["pageContent"]
            util.save_entry(title,content)
            return HttpResponseRedirect(reverse('entry', args=[title]))
    
    precontent = util.get_entry(entryname)
    return render(request,"encyclopedia/editPage.html",{
        "entrytitle": entryname,
        "content": precontent
    })

def randomPage(request):
    entrylist = util.list_entries()
    ranInt = random.randint(0,len(entrylist))
    title = entrylist[ranInt]
    return HttpResponseRedirect(reverse('entry', args=[title]))