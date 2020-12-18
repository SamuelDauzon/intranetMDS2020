# Import
from django.http import HttpResponse

# View
def hello(request):
    return HttpResponse("Hello World!")