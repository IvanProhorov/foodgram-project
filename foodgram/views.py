from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView, View


class FoodgramAuthorView(TemplateView):
    template_name = 'simple_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Об авторе'
        context['text'] = ('Разработчик: Иван Прохоров. '
                           'Github репозиторий: '
                           'https://github.com/IvanProhorov.\r\n'
                           'Docker репозиторий проекта: '
                           'prohivan/foodgram_project')
        return context


class FoodgramTechnologiesView(TemplateView):
    template_name = 'simple_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Технологии'
        context['text'] = ('Технологии используемые в данном проекте '
                           'описаны по адресу: '
                           'https://github.com/IvanProhorov/foodgram-project')
        return context


def page_not_found(request, exception):
    return render(request, 'misc/404.html', {'path': request.path},
                  status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)
