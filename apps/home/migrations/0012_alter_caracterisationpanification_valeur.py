# Generated by Django 3.2.16 on 2023-07-16 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_alter_caracterisationpanification_valeur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caracterisationpanification',
            name='valeur',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=50, null=True),
        ),
    ]
