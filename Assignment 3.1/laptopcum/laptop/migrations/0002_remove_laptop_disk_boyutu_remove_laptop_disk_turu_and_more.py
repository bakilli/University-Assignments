# Generated by Django 4.1.2 on 2022-10-17 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laptop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='laptop',
            name='disk_boyutu',
        ),
        migrations.RemoveField(
            model_name='laptop',
            name='disk_turu',
        ),
        migrations.RemoveField(
            model_name='laptop',
            name='ekran_boyutu',
        ),
        migrations.RemoveField(
            model_name='laptop',
            name='fiyat',
        ),
        migrations.RemoveField(
            model_name='laptop',
            name='isim',
        ),
        migrations.RemoveField(
            model_name='laptop',
            name='islemci_nesli',
        ),
        migrations.RemoveField(
            model_name='laptop',
            name='islemci_tipi',
        ),
        migrations.RemoveField(
            model_name='laptop',
            name='isletim_sistemi',
        ),
        migrations.RemoveField(
            model_name='laptop',
            name='marka',
        ),
        migrations.RemoveField(
            model_name='laptop',
            name='model_adi',
        ),
        migrations.RemoveField(
            model_name='laptop',
            name='model_no',
        ),
        migrations.RemoveField(
            model_name='laptop',
            name='puani',
        ),
        migrations.RemoveField(
            model_name='laptop',
            name='site_ismi',
        ),
        migrations.AddField(
            model_name='laptop',
            name='brand',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='laptop',
            name='cpu',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='laptop',
            name='disc',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='laptop',
            name='disc_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='laptop',
            name='gpu',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='laptop',
            name='model',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='laptop',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='laptop',
            name='operating_system',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='laptop',
            name='price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='laptop',
            name='rating',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='laptop',
            name='screen_size',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='laptop',
            name='site',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='laptop',
            name='site_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='laptop',
            name='ram',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
