from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.upload_view, name='upload'),
    path('success/', views.upload_success, name='upload_success'),  # Add this line
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)