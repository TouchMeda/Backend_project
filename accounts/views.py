from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm



def register(request):
	"""
	Это типичный шаблон view с формой: 
	на GET показываем пустую форму, на POST проверяем данные
	и, если всё верно, сохраняем и делаем редирект.
	"""
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect("server_list")
	else:
		form = UserCreationForm()
	return render(request, "registration/register.html", {"form": form})


