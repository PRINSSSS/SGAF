# Generated by Django 3.2.16 on 2023-07-14 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_alter_caracterisationpanification_valeur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caracterisationpanification',
            name='valeur',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=50, null=True),
        ),
    ]
