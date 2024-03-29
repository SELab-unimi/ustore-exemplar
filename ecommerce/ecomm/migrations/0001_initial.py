# Generated by Django 2.0.7 on 2019-06-15 23:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('ID', models.IntegerField(primary_key=True, serialize=False)),
                ('Quantity', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('ID', models.IntegerField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ConfigFail',
            fields=[
                ('ID', models.IntegerField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=20)),
                ('FailureRateService', models.FloatField(default=0)),
                ('ErrorMessage', models.CharField(default='', max_length=255)),
                ('OkMessage', models.CharField(default='OK', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('ID', models.IntegerField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=255)),
                ('Symbol', models.CharField(default='', max_length=1)),
                ('In_Use', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('ID', models.IntegerField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=255)),
                ('Symbol', models.CharField(default='', max_length=255)),
                ('In_Use', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('ID', models.IntegerField(primary_key=True, serialize=False)),
                ('NameProduct', models.CharField(max_length=255)),
                ('Subtitle', models.CharField(default='', max_length=255)),
                ('Price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('Desc', models.CharField(max_length=255)),
                ('Info', models.CharField(max_length=255)),
                ('Amount', models.IntegerField()),
                ('Sale', models.DecimalField(decimal_places=2, max_digits=5)),
                ('PictureProductName', models.CharField(max_length=255)),
                ('ID_Category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomm.Category')),
            ],
        ),
        migrations.CreateModel(
            name='shipppingAddress',
            fields=[
                ('ID', models.IntegerField(primary_key=True, serialize=False)),
                ('Firstname', models.CharField(default='', max_length=255)),
                ('Lastname', models.CharField(default='', max_length=255)),
                ('Mail', models.CharField(default='', max_length=255)),
                ('Company', models.CharField(default='', max_length=255)),
                ('Street', models.CharField(default='', max_length=255)),
                ('City', models.CharField(default='', max_length=255)),
                ('Zip', models.CharField(default='', max_length=255)),
                ('State', models.CharField(default='', max_length=255)),
                ('Province', models.CharField(default='', max_length=255)),
                ('Phone', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TimeRate',
            fields=[
                ('ID', models.IntegerField(primary_key=True, serialize=False)),
                ('TimeRate', models.FloatField(default=0)),
                ('TimeMin', models.IntegerField(default=0)),
                ('TimeMax', models.IntegerField(default=0)),
                ('ID_ConfigFail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomm.ConfigFail')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('ID', models.IntegerField(primary_key=True, serialize=False)),
                ('Username', models.CharField(default='', max_length=255)),
                ('Name', models.CharField(max_length=255)),
                ('Lastname', models.CharField(default='', max_length=255)),
                ('Mail', models.CharField(default='', max_length=255)),
                ('Password', models.CharField(default='', max_length=255)),
                ('Address', models.CharField(default='', max_length=255)),
                ('isLogged', models.BooleanField(default=False)),
                ('ID_Currency', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ecomm.Currency')),
                ('ID_Language', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ecomm.Language')),
            ],
        ),
        migrations.AddField(
            model_name='shipppingaddress',
            name='ID_User',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ecomm.User'),
        ),
        migrations.AddField(
            model_name='basket',
            name='ID_Product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomm.Product'),
        ),
        migrations.AddField(
            model_name='basket',
            name='ID_User',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomm.User'),
        ),
    ]
