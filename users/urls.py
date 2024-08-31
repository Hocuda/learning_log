from django.urls import path, include

app_name = 'users'
urlpatterns = [
	# Добавить уставные URL auth (аутентификации)
	path('', include('django.contrib.auth.urls')),
]