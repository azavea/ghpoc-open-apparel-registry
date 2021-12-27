# Generated by Django 2.2.24 on 2021-12-09 20:34

from django.db import migrations, models


def set_prefer_contributor_name_false(apps, schema_editor):
    EmbedConfig = apps.get_model('api', 'EmbedConfig')
    for config in EmbedConfig.objects.all():
        config.prefer_contributor_name = False
        config.save()


def do_nothing_on_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0073_add_extended_profile_switch'),
    ]

    operations = [
        migrations.AddField(
            model_name='embedconfig',
            name='prefer_contributor_name',
            field=models.BooleanField(blank=True, help_text="Whether to use the contributor's facility name before other names.", null=True),
        ),
        migrations.RunPython(set_prefer_contributor_name_false, do_nothing_on_reverse)
    ]