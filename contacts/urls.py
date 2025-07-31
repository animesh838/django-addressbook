from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
    # Health check
    path('health/', views.health_check, name='health_check'),
    
    # Regular views
    path('', views.contact_list, name='contact_list'),
    path('create/', views.contact_create, name='contact_create'),
    path('<int:pk>/', views.contact_detail, name='contact_detail'),
    path('<int:pk>/edit/', views.contact_update, name='contact_update'),
    path('<int:pk>/delete/', views.contact_delete, name='contact_delete'),
    
    # API endpoints
    path('api/contacts/', views.api_contact_list, name='api_contact_list'),
    path('api/contacts/create/', views.api_contact_create, name='api_contact_create'),
    path('api/contacts/<int:pk>/update/', views.api_contact_update, name='api_contact_update'),
    path('api/contacts/<int:pk>/delete/', views.api_contact_delete, name='api_contact_delete'),
    path('api/contacts/search/', views.api_contact_detail, name='api_contact_search'),
] 