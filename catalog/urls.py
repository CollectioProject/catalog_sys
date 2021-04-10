from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('about/', views.about, name='catalog-about'),
    path('home/', views.home, name='catalog-home'),
    path('catalog/', views.catalogList, name='catalog-list'),
    path('', RedirectView.as_view(url='about/', permanent=True)),
    path('login/', views.loginPage, name='catalog-login'),
    path('logout/', views.logoutUser, name='catalog-logout'),
    path('register/', views.register, name='catalog-register'),
    path('record/<str:cr>/', views.recordList, name='record-list'),
    path('search/', views.advancedSearch, name='search'),
    path('simpleSearch/', views.simpleSearch, name='simple-search'),
    path('create_record/', views.createRecord, name='record-create'),
    path('create_catalog/', views.createCatalog, name='catalog-create'),
    path('update_record/<str:ur>/', views.updateRecord, name='record-update'),
    path('record_detail/<str:pk>/', views.recordDetail, name='record-detail'),
    path('delete_record/<str:ur>/', views.deleteRecord, name='record-delete'),
]