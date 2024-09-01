from django.urls import path, include

from . import views

app_name = 'users'
urlpatterns = [
	# Добавить уставные URL auth (аутентификации)
	path('', include('django.contrib.auth.urls')),
	# Страница регестрации
	path('register/', views.register, name='register'),
]