# Generated by Django 3.2.16 on 2023-12-18 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizations', '0003_historicalorganizationcourse'),
        ('course_overviews', '0026_courseoverview_entrance_exam'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampusilReportableCoursesDigital',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isReportable', models.BooleanField(default=False)),
                ('course_overview', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course_overviews.courseoverview')),
            ],
        ),
        migrations.CreateModel(
            name='CampusilOrganizationExtension',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(db_column='org_email', max_length=255)),
                ('org_id', models.ForeignKey(db_column='org_id', on_delete=django.db.models.deletion.CASCADE, to='organizations.organization')),
            ],
            options={
                'verbose_name': 'Organization Extension',
                'verbose_name_plural': 'Organizations Extension',
            },
        ),
        migrations.CreateModel(
            name='CampusilOrganizationCourses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.ForeignKey(db_column='course_id', on_delete=django.db.models.deletion.CASCADE, to='course_overviews.courseoverview')),
                ('digital_hub_org_id', models.ForeignKey(db_column='dh_org_id', on_delete=django.db.models.deletion.CASCADE, to='digital_gov_reports.campusilorganizationextension')),
            ],
            options={
                'verbose_name': 'Organization Course',
                'verbose_name_plural': 'Organization Courses',
            },
        ),
    ]
