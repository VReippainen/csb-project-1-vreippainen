from django.urls import path
from . import views

app_name = 'recipe'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/detail', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/edit', views.edit, name='edit'),
    path('add/', views.add, name='add'),
]