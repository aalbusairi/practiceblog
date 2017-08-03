from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Like
from .forms import PostForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib.parse import quote
from django.http import Http404, JsonResponse
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q
from .forms import UserSignup, UserLogin
from django.contrib.auth import authenticate, login, logout

def usersignup(request):
	context = {}
	form = UserSignup()
	context['form'] = form
	if request.method == 'POST':
		form = UserSignup(request.POST)
		if form.is_valid():
			user = form.save()
			username = user.username
			password = user.password

			user.set_password(password)
			user.save()

			auth_user = authenticate(username=username, password=password)
			login(request, auth_user)

			return redirect("posts:list")
		messages.error(request, form.errors)
		return redirect("posts:signup")
	return render(request, 'signup.html', context)

def userlogin(request):
	context = {}
	form = UserLogin()
	context['form'] = form
	if request.method == 'POST':
		form = UserLogin(request.POST)
		if form.is_valid():

			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			auth_user = authenticate(username=username, password=password)
			if auth_user is not None:
				login(request, auth_user)
				return redirect('posts:list')

			messages.error(request, "Wrong username/password combination. Please try again.")
			return redirect("posts:login")
		messages.error(request, form.errors)
		return redirect("posts:login")
	return render(request, 'login.html', context)

def userlogout(request):
	logout(request)
	return redirect("posts:list")
		

def ajax_like(request, post_id):
	post_object = Post.objects.get(id=post_id)
	new_like, created = Like.objects.get_or_create(user=request.user, post=post_object)

	if created:
		action="like"
	else:
		new_like.delete()
		action="unlike"

	post_like_count = post_object.like_set.all().count()
	response = {
		"action": action,
		"post_like_count": post_like_count,
	}
	return JsonResponse(response, safe=False)

def post_create(request):
	if not (request.user.is_staff or request.user.is_superuser):
		raise Http404
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		post = form.save(commit = False)
		post.author = request.user
		form.save()
		messages.success(request, "Succesfuly Created")
		return redirect("posts:list")
	context = {
	"title": "Create",
	"form": form,
	}
	return render(request, 'post_create.html', context)

def post_delete(request, post_slug):
	if not (request.user.is_staff or request.user.is_superuser):
		raise Http404
	instance = get_object_or_404(Post, slug=post_slug)
	instance.delete()
	messages.warning(request, "Succesfully Deleted")
	return redirect("posts:list")

def post_detail(request, post_slug):
	instance = get_object_or_404(Post, slug=post_slug)
	if instance.publish>timezone.now().date() or instance .draft:
		if not (request.user.is_staff or request.user.is_superuser):
			raise Http404
	if request.user.is_authenticated():
		if Like.objects.filter(post=instance, user=request.user).exists():
			liked = True
		else:
			liked = False
	post_like_count = instance.like_set.all().count()

	context = {
	"instance" : instance,
	"share_string": quote(instance.content),
	"post_like_count": post_like_count,
	"liked":liked,
	}
	return render(request, 'post_detail.html', context)

def post_list(request):
	today = timezone.now().date()
	object_list = Post.objects.filter(draft=False).filter(publish__lte=today)
	if request.user.is_staff or request.user.is_superuser:
		object_list = Post.objects.all()

	query = request.GET.get("q")
	if query:
			object_list = object_list.filter(
			Q(title__icontains=query)|
			Q(content__icontains=query)|
			Q(author__first_name__icontains=query)|
			Q(author__last_name__icontains=query)
			).distinct()
			
	paginator = Paginator(object_list, 5)
	page = request.GET.get('page')
	try:
		objects = paginator.page(page)
	except PageNotAnInteger:
		objects=paginator.page(1)
	except EmptyPage:
		objects = paginator.page(paginator.num_pages)		
	context = {
	"object_list": objects,
	"title": "List",
	"user": request.user,
	"today": today,
	}
	return render(request, 'post_list.html', context)

def post_update(request, post_slug):
	if not (request.user.is_staff or request.user.is_superuser):
		raise Http404
	instance = get_object_or_404(Post, slug=post_slug)
	form = PostForm(request.POST or None, request.FILES or None, instance= instance)
	if form.is_valid():
		form.save()
		messages.success(request, "Succesfuly Updated")
		return redirect(instance.get_absolute_url())
	context = {
	"form": form,
	"instance": instance,
	"title": "Update",
	}	
	return render(request, 'post_update.html', context)			