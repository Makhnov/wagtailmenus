from django.db.models import Case, When
from datetime import datetime

from wagtail import hooks
from wagtail.models import Page
try:
    from wagtail_modeladmin.options import modeladmin_register
except ModuleNotFoundError:
    from wagtail.contrib.modeladmin.options import modeladmin_register

from wagtailmenus.conf import settings
from wagtailmenus.utils.misc import derive_section_root
from wagtailmenus.models import ChildrenMenu
from administration.models import ConvocationPage, CompteRenduPage  # Importez vos modèles de page

if settings.MAIN_MENUS_EDITABLE_IN_WAGTAILADMIN:
    modeladmin_register(settings.objects.MAIN_MENUS_MODELADMIN_CLASS)


if settings.FLAT_MENUS_EDITABLE_IN_WAGTAILADMIN:
    modeladmin_register(settings.objects.FLAT_MENUS_MODELADMIN_CLASS)


@hooks.register('before_serve_page')
def wagtailmenu_params_helper(page, request, serve_args, serve_kwargs):
    request.META.update({
        'WAGTAILMENUS_CURRENT_PAGE': page,
        'WAGTAILMENUS_CURRENT_SECTION_ROOT': derive_section_root(page),
    })

# Tri des convocations et des comptes-rendus par date
@hooks.register('menus_modify_raw_menu_items')
def make_some_changes(menu_items, request, menu_instance, original_menu_instance, current_site, **kwargs):
    if isinstance(menu_instance, ChildrenMenu) and original_menu_instance.handle in ['conseil', 'conference', 'bureau', 'commission']:
        type = kwargs.get('parent_context', {}).get('class_type', None)
        child = kwargs.get('parent_context', {}).get('child_type', None)
        print("\033[1;32;41m Instance: ", original_menu_instance.handle, "\033[0m")
        print("Type: ", type)
        print("Child: ", child)
        
        # Séparer les items en ConvocationPage et CompteRenduPage
        convocations = [item for item in menu_items if isinstance(item, ConvocationPage)]
        comptes_rendus = [item for item in menu_items if isinstance(item, CompteRenduPage)]
        
        if type == 'menu':
            print("\033[1;32;41m MENU\033[0m")
            # Trier séparément et combiner
            for item in menu_items:
                if hasattr(item, 'date'):
                    item.item_year = item.date.year
                    # on récupere le mois en toute lettre et pareil pour le jour
                    item.item_month = datetime.strptime(str(item.date.month), "%m").strftime("%B")
                    item.item_day = datetime.strptime(str(item.date.day), "%d").strftime("%A")
                else:
                    item.item_year = None
                    item.item_month = None
                    item.item_day = None
            convocations.sort(key=lambda page: page.date, reverse=True)
            comptes_rendus.sort(key=lambda page: page.date, reverse=True)
            menu_items = convocations + comptes_rendus
            
        elif type == 'nav':
            print("\033[1;32;41m NAV\033[0m")
            # Trier tous ensemble
            if child == 'convocation':
                menu_items = sorted(convocations, key=lambda page: page.date, reverse=True)[:3]
            elif child == 'compte_rendu':   
                menu_items = sorted(comptes_rendus, key=lambda page: page.date, reverse=True)[:3]
                
    return menu_items
