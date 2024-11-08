# Generated by Django 5.0.6 on 2024-10-06 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alternative',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('correct', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('statement', models.TextField()),
                ('explanation', models.TextField()),
                ('score', models.FloatField()),
                ('tagType', models.CharField(choices=[('Numeros', 'Numeros'), ('Geometria', 'Geometria'), ('Álgebra y Funciones', 'Álgebra y Funciones'), ('Probabilidad', 'Probabilidad')], max_length=50)),
                ('alternatives', models.ManyToManyField(to='edugami_app.alternative')),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('questions', models.ManyToManyField(to='edugami_app.question')),
            ],
        ),
    ]
