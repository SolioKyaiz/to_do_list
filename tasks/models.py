from django.db import models
from account.models import User

class Task(models.Model):

    STATUS_CHOICES = [
        ("To Do", 'К выполнению'),
        ("In Progress", 'В Процессе'),
        ("In Review", 'На Проверке'),
        ("Done", 'Выполнено'),
    ]

    PRIORITY_CHOICES = [
        ('Low','Низкий'),
        ('Medium','Средний'),
        ('High','Высокий')
    ]
    owner = models.ForeignKey(
        to=User,
        on_delete = models.CASCADE,
        verbose_name='Автор',
        related_name='tasks'
    )

    title =models.CharField(
        max_length=255,
        verbose_name="Название"
    )
    description = models.CharField(
        max_length=255,
        verbose_name="Описание",
        blank=True,
        null = True
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='Medium',
        verbose_name = 'Приоритет'
    )

    deadline = models.DateTimeField(verbose_name='Дедлайн')

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='To Do',
        verbose_name = 'Статус'
    )

    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Дата создания")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['deadline']
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"




