from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_view, name='home'),  # Home page route
    path('upload/', views.file_upload_view, name='file_upload'),  # File upload page
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
