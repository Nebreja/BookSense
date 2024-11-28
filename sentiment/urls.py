from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_view, name='home'),  # Home page route
    path('upload/', views.file_upload_view, name='file_upload'),  # File upload page
    path('user/files/', views.user_uploaded_files, name='user_files'),
    path('view_analysis_result/<int:file_id>/', views.view_analysis_result, name='view_analysis_result'),
    path('delete_file/<int:file_id>/', views.delete_uploaded_file, name='delete_file'),
    path('signup/', views.signup_view, name='signup'),
    path('signin/', views.signin_view, name='signin'),
    path('logout/', views.logout_view, name='logout'),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
