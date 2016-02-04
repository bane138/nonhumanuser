from django.shortcuts import render

# Create your views here.
def index(request):
	context = {
		"site": { 
			"title": "Non Human User",
			"description": "Stories, articles resources and supplements for Call of Cthulhu and related genre games." 
		}
	}
	return render(request, 'app/index.html', context)