from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView,
)

from .models import Server

SERVER_FIELDS = ["hostname", "ip_address", "os", "status", "tags"]


class ServerListView(LoginRequiredMixin, ListView):
    model = Server

    def get_queryset(self):

        return Server.objects.select_related("owner").prefetch_related("tags")


class ServerDetailView(LoginRequiredMixin, DetailView):
    model = Server

    def get_queryset(self):
        return Server.objects.select_related("owner").prefetch_related("tags", "incidents")


class ServerCreateView(PermissionRequiredMixin, CreateView):
    model = Server
    fields = SERVER_FIELDS
    permission_required = "inventory.add_server"
    template_name = "form.html"
    success_url = reverse_lazy("server_list")
    extra_context = {"title": "Новый сервер"}

    def form_valid(self, form):
        form.instance.owner = self.request.user # владелец = текущий пользователь
        return super().form_valid(form)


class ServerUpdateView(PermissionRequiredMixin, UpdateView):
    model = Server
    fields = SERVER_FIELDS
    permission_required = "inventory.change_server"
    template_name = "form.html"
    success_url = reverse_lazy("server_list")
    extra_context = {"title": "Редактирование сервера"}


class ServerDeleteView(PermissionRequiredMixin, DeleteView):
    model = Server
    permission_required = "inventory.delete_server"
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("server_list")


