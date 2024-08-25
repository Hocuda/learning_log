from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
	"""Главная страница 'Журнала наблюдений' """
	return render(request, 'learning_logs/index.html')

def topics(request):
	"""Отображает все темы"""
	topics = Topic.objects.order_by('date_added')
	context = {'topics': topics}
	return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
	"""Показать отдельный раздел и все его записи"""
	topic = Topic.objects.get(id=topic_id)
	entries = topic.entry_set.order_by('-date_added')
	context = {'topic': topic, 'entries': entries}
	return render(request, 'learning_logs/topic.html', context)

def new_topic(request):
	"""Добавить новую тему"""
	if request.method != 'POST':
		# Никаких данных не отправленно; создать пустую форму
		form = TopicForm()
	else:
		# Полученны данные в POST формате; обработать данные
		form = TopicForm(data=request.POST)
		if form.is_valid():
			form.save()
			return redirect('learning_logs:topics')

	# Показать пустую или недействительную форму
	context = {'form': form}
	return render(request, 'learning_logs/new_topic.html', context)

def new_entry(request, topic_id):
	"""Добавить новую запись в конкретную тему"""
	topic = Topic.objects.get(id=topic_id)
	if request.method != 'POST':
		# Никаких данных не отправленно; создать пустую форму
		form = EntryForm()
	else:
		# Полученны данные в POST формате; обработать данные
		form = EntryForm(data=request.POST)
		if form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.topic = topic
			new_entry.save()
			return redirect('learning_logs:topic', topic_id=topic_id)

	# Показать пустую или недецствительную форму
	context = {'topic': topic, 'form': form}
	return render(request, 'learning_logs/new_entry.html', context)

def edit_entry(request, entry_id):
	"""Редактировать сущевствующую модель"""
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic

	if request.method != 'POST':
		# Исходній запрос, заполнить форму существующей записью
		form = EntryForm(instance=entry)
	else:
		# POST пакет принят, обработка данных
		form = EntryForm(instance=entry, data=request.POST)
		if form.is_valid():
			form.save()
			return redirect('learning_logs:topic', topic.id)

	context = {'entry': entry, 'topic': topic, 'form': form}
	return render(request, 'learning_logs/edit_entry.html', context)