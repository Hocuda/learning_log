from django.shortcuts import render

def index(request):
	"""Главная страница 'Журнала наблюдений' """
	return render(request, 'learning_logs/index.html')