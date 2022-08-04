# Generated by Django 3.2.4 on 2022-07-27 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0098_add_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContributorWebhook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(help_text='The URL of the web hook')),
                ('notification_type', models.CharField(choices=[('ALL_FACILITIES', 'ALL_FACILITIES'), ('ASSOCIATED', 'ASSOCIATED')], help_text='Whether to send notifications for all events or only events for associated facilities.', max_length=15)),
                ('filter_query_string', models.TextField(blank=True, default='', help_text='A query string search filter that will be applied before sending notification events')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('contributor', models.ForeignKey(help_text='The contributor who configured this webhook.', on_delete=django.db.models.deletion.CASCADE, to='api.contributor')),
            ],
        ),
    ]
