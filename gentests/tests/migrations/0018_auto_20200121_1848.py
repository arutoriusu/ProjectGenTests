# Generated by Django 2.2.7 on 2020-01-21 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0017_auto_20200121_0224'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variant',
            name='number_of_variants',
        ),
        migrations.AddField(
            model_name='variant',
            name='number_of_variant',
            field=models.CharField(default='1', max_length=2),
        ),
        migrations.AlterField(
            model_name='variant',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='tests.Test'),
        ),
    ]