# Generated by Django 4.0.3 on 2022-11-04 22:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('apellido_pat', models.CharField(max_length=20)),
                ('apellido_mat', models.CharField(max_length=20)),
                ('grado', models.CharField(max_length=30)),
                ('institucion', models.CharField(max_length=60)),
                ('departamento', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='ContactoPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40)),
                ('text', models.CharField(max_length=300)),
                ('contacto', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='EdicionesPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40)),
                ('text', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.IntegerField()),
                ('year', models.IntegerField()),
                ('cartel', models.FileField(blank=True, null=True, upload_to='base/')),
                ('plantilla_constancias_img', models.ImageField(blank=True, null=True, upload_to='constancias/base/')),
                ('correo_comunicacion', models.EmailField(blank=True, max_length=254, null=True)),
                ('correo_contrasena', models.CharField(blank=True, max_length=100, null=True)),
                ('contacto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='TestApp.contactopage')),
                ('edicion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='TestApp.edicionespage')),
            ],
        ),
        migrations.CreateModel(
            name='InicioPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_descripcion', models.CharField(max_length=40)),
                ('text_descripcion', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='PosterPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poster_img', models.ImageField(upload_to='archivos/')),
            ],
        ),
        migrations.CreateModel(
            name='ProgramaPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('programa_pdf', models.FileField(upload_to='TestApp/static/TestApp/archivos/')),
                ('programa_img', models.ImageField(upload_to='archivos/')),
            ],
        ),
        migrations.CreateModel(
            name='RegistroPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_participacion_ponente', models.CharField(max_length=40)),
                ('text_participacion_ponente', models.CharField(max_length=300)),
                ('title_formato_resumen', models.CharField(max_length=40)),
                ('text_formato_resumen', models.CharField(max_length=300)),
                ('title_constancias_participacion', models.CharField(max_length=40)),
                ('text_constancias_participacion', models.CharField(max_length=300)),
                ('title_participacion_asistente', models.CharField(max_length=40)),
                ('text_participacion_asistente', models.CharField(max_length=300)),
                ('formato_resumen_pdf', models.FileField(upload_to='registros/resumenes/')),
            ],
        ),
        migrations.CreateModel(
            name='UbicacionPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40)),
                ('text', models.CharField(max_length=300)),
                ('url_maps_embed', models.URLField(max_length=250)),
                ('url_maps', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='PresentacionRegistro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('presentacion_titulo', models.CharField(max_length=40)),
                ('resp_email', models.EmailField(max_length=254)),
                ('modalidad', models.CharField(max_length=30)),
                ('resumen', models.FileField(upload_to='registros/resumenes/')),
                ('estatus', models.CharField(max_length=30)),
                ('a1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='a1', to='TestApp.author')),
                ('a2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='a2', to='TestApp.author')),
                ('a3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='a3', to='TestApp.author')),
                ('a4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='a4', to='TestApp.author')),
                ('a5', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='a5', to='TestApp.author')),
                ('a6', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='a6', to='TestApp.author')),
                ('a7', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='a7', to='TestApp.author')),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TestApp.evento')),
                ('resp', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='resp', to='TestApp.author')),
            ],
        ),
        migrations.AddField(
            model_name='evento',
            name='inicio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='TestApp.iniciopage'),
        ),
        migrations.AddField(
            model_name='evento',
            name='poster',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='TestApp.posterpage'),
        ),
        migrations.AddField(
            model_name='evento',
            name='programa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='TestApp.programapage'),
        ),
        migrations.AddField(
            model_name='evento',
            name='registro',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='TestApp.registropage'),
        ),
        migrations.AddField(
            model_name='evento',
            name='ubicacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='TestApp.ubicacionpage'),
        ),
    ]
