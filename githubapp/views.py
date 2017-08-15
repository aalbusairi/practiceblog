from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
import requests

def org_members(request):
	user = request.user
	social_account = user.socialaccount_set.get(user=user.id)
	token = social_account.socialtoken_set.get(account=social_account.id).token

	url = "https://api.github.com/orgs/joinCODED/members"
	response = requests.get(url, headers={"Authorization":"token "+token})
	# return JsonResponse(response.json(), safe=False)

	context = {
	"response":response.json(),
	}

	return render(request, 'org_members.html', context)

def listbranches(request):
	user = request.user
	social_account = user.socialaccount_set.get(user=user.id)
	repo = "blog"
	token = social_account.socialtoken_set.get(account=social_account.id).token	

	url = "https://api.github.com/repos/%s/%s/branches"%(user, repo)
	response = requests.get(url, headers={"Authorization":"token "+token})

	# return JsonResponse(response.json(), safe=False)

	context = {
	"response":response.json(),
	}

	return render(request, 'listbranches.html', context)


