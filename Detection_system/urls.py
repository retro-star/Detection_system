from django.urls import path,include
from myapp import urls
import myapp
urlpatterns = [
    path('', include(myapp.urls)),
]
