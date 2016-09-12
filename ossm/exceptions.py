from django.http import HttpResponse

class Http409(HttpResponse):
    status_code = 409
