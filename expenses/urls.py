from django.contrib import admin
from django.urls import path
from expenses import settings
from django.conf.urls.static import static
from app import views, views_auth

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('register/', views_auth.registration, name='register'),
    path('login/', views_auth.login_view, name='login'),
    path('logout/', views_auth.logout_view, name='logout'),
    path('account/', views.account, name='account'),
    path('create/', views.create_views, name='create'),
    path('delete/<int:transaction_id>', views.delete_views, name='delete'),
    path('edit/<int:transaction_id>', views.edit_views, name='edit'),
    path('add_10', views.add10, name='add10'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

