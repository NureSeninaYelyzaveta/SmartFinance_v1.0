from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('transactions/', views.transactions_view, name='transactions'),
    path('categories/', views.categories_view, name='categories'),
    path('goals/', views.goals_view, name='goals'),
    path('reports/', views.reports_view, name='reports'),
    path('accounts/', include('django.contrib.auth.urls')), 
    path('accounts/register/', views.register, name='register'),
    path('profile/', views.profile_view, name='profile'),
     path('lang/<str:lang>/', views.set_language, name='set_language'),

      path('transaction/edit/<int:pk>/', views.edit_transaction, name='edit_transaction'),
    path('transaction/delete/<int:pk>/', views.delete_transaction, name='delete_transaction'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


