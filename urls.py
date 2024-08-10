from django.urls import path
from . import views
urlpatterns = [
    path('', views.Home,name="Home"),
    path('delete/<int:note_id>', views.Delete, name="delete"),
    path('edit/<int:note_id>', views.Edit, name="Edit"),
    path('notes/', views.Notes, name="Notes"),
    path('login/', views.Login, name="Login"),
    path('create/', views.Create, name="Create"),
    path('signup/', views.Signup, name="Signup"),
    path('logout/', views.Logout, name="Logout"),
    path('setfav/<int:note_id>', views.SetFav, name="SetFav"),
    path('viewnote/<int:note_id>', views.ViewNote, name="ViewNote"),
]