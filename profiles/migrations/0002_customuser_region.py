# Generated by Django 2.1.4 on 2018-12-18 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '0007_auto_20181218_1130'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='regions.Region'),
        ),
    ]