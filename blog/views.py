from django.urls import reverse_lazy, reverse

from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.models import Blog


class BlogCreateView(CreateView):
    """Контроллер создания статьи (после создания переходим на вкладку Блог"""
    model = Blog
    fields = ('title', 'body', 'preview', 'date_of_creation', 'is_published',)
    success_url = reverse_lazy('blog:list')
    permission_required = 'blog.set_is_activated'

    def form_valid(self, form):
        """Формируем динамический slug-name"""

        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)


class BlogListView(ListView):
    """Контроллер для вывода списка статей блога"""
    model = Blog

    """Контроллер для вывода в список статей только те, 
    которые имеют положительный признак публикации"""
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    """Контроллер для вывода детальной информации о статье"""
    model = Blog
    permission_required = 'blog:view'

    def get_object(self, queryset=None):
        """Изменение счетчика просмотра статьи"""
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()

        return self.object


class BlogUpdateView(UpdateView):
    """Контроллер для редактирования статьи"""
    model = Blog
    fields = ('title', 'body', 'preview', 'date_of_creation', 'is_published',)
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        """Формируем динамический slug-name"""

        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('pk')])


class BlogDeleteView(DeleteView):
    """Контроллер для удаления статьи"""
    model = Blog
    success_url = reverse_lazy('blog:list')
