# Generated by Django 3.2.16 on 2023-11-28 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ccx', '0007_customcourseforedx_coach2'),
        ('ccx_customizations', '0002_alter_origin_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customcourseforedxextradata',
            options={'verbose_name': 'CCX Extra Data', 'verbose_name_plural': 'CCX Extra Data'},
        ),
        migrations.AlterModelOptions(
            name='origin',
            options={'verbose_name': 'CCX Origin', 'verbose_name_plural': 'CCX Origins'},
        ),
        migrations.AlterField(
            model_name='customcourseforedxextradata',
            name='ccx_course',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ccx_extra_data', to='ccx.customcourseforedx'),
        ),
    ]
