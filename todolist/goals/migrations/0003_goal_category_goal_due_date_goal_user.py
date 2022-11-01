# Generated by Django 4.0.1 on 2022-10-25 16:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goals', '0002_goal'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='goals',
                                    to='goals.goalcategory', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='goal',
            name='due_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата выполнения'),
        ),
        migrations.AddField(
            model_name='goal',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='goals',
                                    to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
    ]
