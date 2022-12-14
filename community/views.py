from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import  *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .utils import searchPost, paginationPosts
from django.contrib import messages

# Create your views here.

def post(request):
    projects, search_query = searchPost(request)
    custom_range, projects = paginationPosts(request, projects, 6)
    context={'post': projects, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'community/posts.html', context)
    
@login_required(login_url="login")
def posts(request, pk):
    projectObj = Post.objects.get(id = pk)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        comment = form.save(commit=False)
        comment.post_id = projectObj
        comment.owner = request.user.profile
        comment.save()
        projectObj.getVoteCount
        messages.success(request, "Comment was successfully submitted!")
        return redirect('posts', pk=projectObj.id)

    return render(request, 'community/single-posts.html',  {"posts": projectObj, 'form': form})

@login_required(login_url="login")
def createPost(request):
    profile = request.user.profile
    form = PostForm()
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', " ").split()
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = profile
            post.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                post.tags.add(tag)
            return redirect("post")
    


    context={'form': form}
    return render(request, "community/post_form.html", context)


@login_required(login_url="login")
def updatePost(request,pk):
    profile = request.user.profile
    project = profile.post_set.get(id = pk)
    form = PostForm(instance = project)
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', " ").split()
        form = PostForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('post')
    
    context={'form': form, 'project': project}
    return render(request, "community/post_form.html", context)


@login_required(login_url="login")
def deletePost(request, pk):
    profile = request.user.profile
    project = profile.post_set.get(id = pk)
    if request.method == "POST":
        project.delete()
        return redirect('post')
    context = {"object": project}
    return render(request, 'delete_object.html', context)


def removeTag(request):
    tagId = request.data['tag']
    projectId = request.data['project']

    project = Post.objects.get(id = projectId)
    tag = Tag.objects.get(id = tagId)

    project.tags.remove(tag)
    return 