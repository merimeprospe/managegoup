# Generated by Django 4.0.4 on 2022-06-24 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projet', '0007_alter_tache_decision_log'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='user_projet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projet_to_user', to='projet.project'),
        ),
    ]
