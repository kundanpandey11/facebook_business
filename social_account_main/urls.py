from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('facebook.urls'), name='facebook-urls'),
    path("scrape-facebook", include('scrape_facebook.urls'), name='scrape_faceboook'),
    #Adding social auth path
    path('social-auth/', include('social_django.urls', namespace="social")),
    
   
    
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
