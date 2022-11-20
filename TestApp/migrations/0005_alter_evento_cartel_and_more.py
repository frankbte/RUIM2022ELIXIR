# Generated by Django 4.1.1 on 2022-11-20 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("TestApp", "0004_alter_evento_plantilla_constancias_img_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="evento",
            name="cartel",
            field=models.FileField(blank=True, null=True, upload_to="admin/"),
        ),
        migrations.AlterField(
            model_name="evento",
            name="plantilla_constancias_img",
            field=models.ImageField(blank=True, null=True, upload_to="admin/"),
        ),
        migrations.AlterField(
            model_name="posterpage",
            name="poster_img",
            field=models.ImageField(upload_to="admin/"),
        ),
        migrations.AlterField(
            model_name="posterpage",
            name="poster_pdf",
            field=models.FileField(upload_to="admin/"),
        ),
        migrations.AlterField(
            model_name="programapage",
            name="programa_img",
            field=models.ImageField(upload_to="admin/"),
        ),
        migrations.AlterField(
            model_name="programapage",
            name="programa_pdf",
            field=models.FileField(upload_to="admin/"),
        ),
        migrations.AlterField(
            model_name="registropage",
            name="formato_resumen_pdf",
            field=models.FileField(upload_to="admin/"),
        ),
    ]
