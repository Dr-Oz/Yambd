# Generated by Django 3.2.8 on 2023-05-03 06:58

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import review.validators


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('year', models.IntegerField(validators=[review.validators.validate_year], verbose_name='год')),
                ('description', models.TextField(blank=True, max_length=255, null=True, verbose_name='описание')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='review.category', verbose_name='категория')),
                ('genre', models.ManyToManyField(related_name='titles', to='review.Genre', verbose_name='жанр')),
            ],
            options={
                'verbose_name': 'Произведение',
                'verbose_name_plural': 'Произведения',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('score', models.IntegerField(error_messages={'validators': 'Оценка от 1 до 10!'}, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='оценка')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='дата публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='автор')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='review.title', verbose_name='произведение')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ('pub_date',),
            },
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('title', 'author'), name='unique review'),
        ),
    ]