# Generated by Django 2.0.13 on 2019-06-10 19:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_contributor_add_verified_fields_and_history_20190605'),
    ]

    operations = [
        migrations.AddField(
            model_name='facilityclaim',
            name='status_change_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='historicalfacilityclaim',
            name='status_change_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.CreateModel(
            name='FacilityClaimReviewNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(help_text='The review note')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(help_text='The author of the facility claim review note', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalFacilityClaimReviewNote',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('note', models.TextField(help_text='The review note')),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('author', models.ForeignKey(blank=True, db_constraint=False, help_text='The author of the facility claim review note', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical facility claim review note',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.AddField(
            model_name='facilityclaim',
            name='status_change_by',
            field=models.ForeignKey(help_text='The user who changed the status of this facility claim', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='approver_of_claim', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='facilityclaim',
            name='status_change_reason',
            field=models.TextField(blank=True, help_text='The reason entered when changing the status of this claim.', null=True),
        ),
        migrations.AddField(
            model_name='historicalfacilityclaim',
            name='status_change_by',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='The user who changed the status of this facility claim', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalfacilityclaim',
            name='status_change_reason',
            field=models.TextField(blank=True, help_text='The reason entered when changing the status of this claim.', null=True),
        ),
        migrations.AddField(
            model_name='historicalfacilityclaimreviewnote',
            name='claim',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='The facility claim for this note', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='api.FacilityClaim'),
        ),
        migrations.AddField(
            model_name='historicalfacilityclaimreviewnote',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='facilityclaimreviewnote',
            name='claim',
            field=models.ForeignKey(help_text='The facility claim for this note', on_delete=django.db.models.deletion.PROTECT, to='api.FacilityClaim'),
        ),
    ]
