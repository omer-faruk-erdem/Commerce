# Generated by Django 3.2.22 on 2023-10-17 20:29

import auctions.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=64)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='id',
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=64, primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=1024)),
                ('image', models.ImageField(default='images/default.jpg', upload_to='images/')),
                ('bottom_price', models.IntegerField(default=0)),
                ('bid_count', models.IntegerField(default=0)),
                ('date', models.DateTimeField(default=auctions.models.current_date)),
                ('date_string', models.CharField(default=auctions.models.date_string, max_length=64)),
                ('is_active_listing', models.BooleanField(default=True)),
                ('category', models.ForeignKey(default=auctions.models.Category.get_default_category, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='listings', to='auctions.category')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', to=settings.AUTH_USER_MODEL)),
                ('watch_listed', models.ManyToManyField(default=None, related_name='watch_list', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('comment_text', models.CharField(default='DEFAULT COMMENT', max_length=256)),
                ('related_listing', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='auctions.listing')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('value', models.IntegerField()),
                ('owner', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='bids', to=settings.AUTH_USER_MODEL)),
                ('related_listing', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='bid', to='auctions.listing')),
            ],
        ),
    ]