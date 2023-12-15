from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='название')
    slug = models.CharField(max_length=100, verbose_name='slug', **NULLABLE)
    body = models.TextField(verbose_name='содержимое')
    preview = models.ImageField(upload_to='blog/', verbose_name='превью', **NULLABLE)
    date_of_creation = models.DateField(verbose_name='дата создания', **NULLABLE)
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')
    views_count = models.IntegerField(default=0, verbose_name='количество просмотров')

    def __str__(self):
        return self.title

    class Meta():
        verbose_name = 'блоговая запись'
        verbose_name_plural = 'блоговые записи'