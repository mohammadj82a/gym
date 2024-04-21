from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
   
    path('', views.main, name='main'),
    path('status/', views.status, name='status'),
    path('singup/main.html', views.main, name='main2'),
    path('detail/<int:pk>/main.html', views.main, name='main25'),

    path('edit/<int:pk>/gymodel_detail.html', views.gymodel_detail, name='main3'),
    path('singup/', views.gymodel_create, name='gymodel-create'),
    path('edit/<int:pk>/', views.gymodel_edit, name='gymodel-edit'),
    path('detail/<int:pk>/', views.gymodel_edit, name='gymodel-detail'),
    path('gymodel/<int:pk>/delete/', views.gymodelDeleteView.as_view(), name='gymmodel-delete'),
    path('search/', views.search_view, name='search_view'),
    path('results/', views.search_results, name='search_results'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('reload-models/', views.reload_models, name='reload_models'),


]