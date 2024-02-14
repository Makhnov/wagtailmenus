# Generated by Django 5.0 on 2024-02-14 11:16

import django.db.models.deletion
import modelcluster.fields
import wagtailmenus.models.menuitems
import wagtailmenus.models.menus
import wagtailmenus.models.mixins
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0092_query_searchpromotion_querydailyhits'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlatMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='For internal reference only.', max_length=255, verbose_name='title')),
                ('handle', models.SlugField(help_text='Used to reference this menu in templates etc. Must be unique for the selected site.', max_length=100, verbose_name='handle')),
                ('heading', models.CharField(blank=True, help_text='If supplied, appears above the menu when rendered.', max_length=255, verbose_name='heading')),
                ('max_levels', models.PositiveSmallIntegerField(choices=[(1, '1: No sub-navigation (flat)'), (2, '2: Allow 1 level of sub-navigation'), (3, '3: Allow 2 levels of sub-navigation'), (4, '4: Allow 3 levels of sub-navigation')], default=1, help_text='The maximum number of levels to display when rendering this menu. The value can be overidden by supplying a different <code>max_levels</code> value to the <code>{% flat_menu %}</code> tag in your templates.', verbose_name='maximum levels')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.site', verbose_name='site')),
            ],
            options={
                'verbose_name': 'flat menu',
                'verbose_name_plural': 'flat menus',
                'abstract': False,
                'unique_together': {('site', 'handle')},
            },
            bases=(wagtailmenus.models.mixins.DefinesSubMenuTemplatesMixin, models.Model, wagtailmenus.models.menus.Menu),
        ),
        migrations.CreateModel(
            name='FlatMenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('link_url', models.CharField(blank=True, max_length=255, null=True, verbose_name='link to a custom URL')),
                ('url_append', models.CharField(blank=True, help_text="Use this to optionally append a #hash or querystring to the above page's URL.", max_length=255, verbose_name='append to URL')),
                ('handle', models.CharField(blank=True, help_text='Use this field to optionally specify an additional value for each menu item, which you can then reference in custom menu templates.', max_length=100, verbose_name='handle')),
                ('link_text', models.CharField(blank=True, help_text="Provide the text to use for a custom URL, or set on an internal page link to use instead of the page's title.", max_length=255, verbose_name='link text')),
                ('allow_subnav', models.BooleanField(default=False, help_text="NOTE: The sub-menu might not be displayed, even if checked. It depends on how the menu is used in this project's templates.", verbose_name='allow sub-menu for this item')),
                ('link_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.page', verbose_name='link to an internal page')),
                ('menu', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='wagtailmenus.flatmenu')),
            ],
            options={
                'verbose_name': 'menu item',
                'verbose_name_plural': 'menu items',
                'ordering': ('sort_order',),
                'abstract': False,
            },
            bases=(models.Model, wagtailmenus.models.menuitems.MenuItem),
        ),
        migrations.CreateModel(
            name='MainMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_levels', models.PositiveSmallIntegerField(choices=[(1, '1: No sub-navigation (flat)'), (2, '2: Allow 1 level of sub-navigation'), (3, '3: Allow 2 levels of sub-navigation'), (4, '4: Allow 3 levels of sub-navigation')], default=2, help_text='The maximum number of levels to display when rendering this menu. The value can be overidden by supplying a different <code>max_levels</code> value to the <code>{% main_menu %}</code> tag in your templates.', verbose_name='maximum levels')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.site', verbose_name='site')),
            ],
            options={
                'verbose_name': 'main menu',
                'verbose_name_plural': 'main menu',
                'abstract': False,
            },
            bases=(wagtailmenus.models.mixins.DefinesSubMenuTemplatesMixin, models.Model, wagtailmenus.models.menus.Menu),
        ),
        migrations.CreateModel(
            name='MainMenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('link_url', models.CharField(blank=True, max_length=255, null=True, verbose_name='link to a custom URL')),
                ('url_append', models.CharField(blank=True, help_text="Use this to optionally append a #hash or querystring to the above page's URL.", max_length=255, verbose_name='append to URL')),
                ('handle', models.CharField(blank=True, help_text='Use this field to optionally specify an additional value for each menu item, which you can then reference in custom menu templates.', max_length=100, verbose_name='handle')),
                ('link_text', models.CharField(blank=True, help_text="Provide the text to use for a custom URL, or set on an internal page link to use instead of the page's title.", max_length=255, verbose_name='link text')),
                ('allow_subnav', models.BooleanField(default=True, help_text="NOTE: The sub-menu might not be displayed, even if checked. It depends on how the menu is used in this project's templates.", verbose_name='allow sub-menu for this item')),
                ('link_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.page', verbose_name='link to an internal page')),
                ('menu', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='wagtailmenus.mainmenu')),
            ],
            options={
                'verbose_name': 'menu item',
                'verbose_name_plural': 'menu items',
                'ordering': ('sort_order',),
                'abstract': False,
            },
            bases=(models.Model, wagtailmenus.models.menuitems.MenuItem),
        ),
    ]
