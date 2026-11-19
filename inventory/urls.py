from django.urls import path
from . import views

urlpatterns = [
    path("", views.ServerListView.as_view(), name="server_list"),
    path("add/", views.ServerCreateView.as_view(), name="server_add"),
    path("<int:pk>/", views.ServerDetailView.as_view(), name="server_detail"),
    path("<int:pk>/edit/", views.ServerUpdateView.as_view(), name="server_edit"),
    path("<int:pk>/delete/", 
    	views.ServerDeleteView.as_view(),
    	name="server_delete"
    ),
]
