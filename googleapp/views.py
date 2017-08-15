from django.shortcuts import render
from django.http import JsonResponse
import requests

def text_search(request):
	api_key = "AIzaSyAOuEU_qz6RyeuvfDpLw0IaDSywp46Rtu0"
	query = request.GET.get("query", '')
	next_page_token = request.GET.get("next_page_token")
	url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&key=%s'%(query, api_key)
	
	if next_page_token is not None:
			url += "&pagetoken=%s"%(next_page_token)

	response = requests.get(url)
	
	context = {
		"response":response.json(),
	}
	return render(request, 'text.html', context)

def place_detail(request):
	api_key = "AIzaSyAOuEU_qz6RyeuvfDpLw0IaDSywp46Rtu0"
	query = request.GET.get("reference")
	key = 'AIzaSyDBzLV40ne47V_C50u34jQBnM6zVHeZ-Hc'
	url = "https://maps.googleapis.com/maps/api/place/details/json?reference=%s&key=%s"%(query, api_key)
	response = requests.get(url)

	context = {
		"response": response.json(),
		"key": key,
	}

	return render(request, 'detail.html', context)

def nearby_search(request):
	api_key = "AIzaSyAOuEU_qz6RyeuvfDpLw0IaDSywp46Rtu0"
	location = request.GET.get("location")
	radius = request.GET.get("radius", '')
	# url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-33.8670522,151.1957362&radius=500&key=AIzaSyAOuEU_qz6RyeuvfDpLw0IaDSywp46Rtu0"
	url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s&radius=%s&key=%s'%(location, radius, api_key)
	response = requests.get(url)

	context = {
		"response":response.json(),
	}

	return render(request, 'nearby.html', context)
