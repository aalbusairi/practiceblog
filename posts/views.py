from django.shortcuts import render
from .models import Post

def post_create(request):
	return render(request, 'post_create.html', {})

def post_delete(request):
	return render(request, 'post_delete.html', {})

def post_detail(request):
	return render(request, 'post_detail.html', {})

def post_list(request):
	object_list = Post.objects.all()
	context = {
	"object_list": object_list
	}
	return render(request, 'post_list.html', context)

def post_update(request):
	return render(request, 'post_update.html', {})			