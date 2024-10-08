from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
	"""Тема, которую проходит пользователь"""
	text = models.CharField(max_length=200)
	date_added = models.DateTimeField(auto_now_add=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	private = models.BooleanField()

	def __str__(self):
		"""Вернуть строчное представление модели"""
		return self.text

class Entry(models.Model):
	"""Конкретная информация к теме"""
	topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
	text = models.TextField()
	date_added  = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = 'entries'


	def __str__(self):
		"""Возвращает представление модели в string"""
		if len(self.text) >= 50:
			return f"{self.text[:50]}..."
		else:
			return f"{self.text}"