from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
	"""Главная страница 'Журнала наблюдений' """
	return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
	"""Отображает все темы"""
	topics = Topic.objects.filter(owner=request.user).order_by('date_added')
	context = {'topics': topics}
	return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
	"""Показать отдельный раздел и все его записи"""
	topic = get_object_or_404(Topic, id=topic_id)
	if topic.owner != request.user:
		raise Http404
	entries = topic.entry_set.order_by('-date_added')
	context = {'topic': topic, 'entries': entries}
	return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
	"""Добавить новую тему"""
	if request.method != 'POST':
		# Никаких данных не отправленно; создать пустую форму
		form = TopicForm()
	else:
		# Полученны данные в POST формате; обработать данные
		form = TopicForm(data=request.POST)
		if form.is_valid():
			new_topic = form.save(commit=False)
			new_topic.owner = request.user
			new_topic.save()
			return redirect('learning_logs:topics')

	# Показать пустую или недействительную форму
	context = {'form': form}
	return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
	"""Добавить новую запись в конкретную тему"""
	topic = get_object_or_404(Topic, id=topic_id)
	if topic.owner != request.user:
		raise Http404
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


@login_required
def edit_entry(request, entry_id):
	"""Редактировать сущевствующую модель"""
	entry = get_object_or_404(Entry, id=entry_id)
	topic = entry.topic
	if topic.owner != request.user:
		raise Http404

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