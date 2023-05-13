from django.urls import path 
from . import views 


urlpatterns = [ 
    path('', views.get_page_url, name='get-page-url'),
    path("create-new-request", views.create_request, name="create-request"),
]