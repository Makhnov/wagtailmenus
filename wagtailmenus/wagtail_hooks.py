from datetime import datetime
from django.utils import timezone
from termcolor import colored
from wagtail import hooks

from wagtail_modeladmin.options import modeladmin_register
from wagtailmenus.conf import settings
from wagtailmenus.utils.misc import derive_section_root
from wagtailmenus.models import ChildrenMenu, FlatMenu
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
def update_cv_cr_list(menu_items, request, menu_instance, original_menu_instance, current_site, **kwargs):
    # Variables statiques pour stocker les convocations et comptes-rendus
    if not hasattr(update_cv_cr_list, 'previous_conv'):
        update_cv_cr_list.previous_conv = []
    if not hasattr(update_cv_cr_list, 'previous_cr'):
        update_cv_cr_list.previous_cr = []
        
    if (isinstance(menu_instance, ChildrenMenu) and original_menu_instance.handle in ['administration', 'conseil', 'conference', 'bureau', 'commission']):
        # print(colored(f'Instance: {original_menu_instance.handle}', 'white', 'on_blue'))   
        type = kwargs.get('parent_context', {}).get('class_type', None)
        child = kwargs.get('parent_context', {}).get('child_type', None)
        items_number = kwargs.get('parent_context', {}).get('items_number', None)
        # Séparer les items en ConvocationPage et CompteRenduPage
        convocations = [item for item in menu_items if isinstance(item, ConvocationPage)]
        comptes_rendus = [item for item in menu_items if isinstance(item, CompteRenduPage)]
                
        if items_number == "1" or items_number == "2":
            # on transforme items_number en int
            items_number = int(items_number)   
            if child == 'cv_cr':
                # Ajout des éléments de la page soeur précédente
                convocations += update_cv_cr_list.previous_conv
                comptes_rendus += update_cv_cr_list.previous_cr   
                # Définir la date actuelle
                current_date = timezone.now()                                 
                # Filtrer et trier les convocations pour les dates futures
                future_convocations = [conv for conv in convocations if conv.date > current_date]
                future_convocations.sort(key=lambda page: page.date)
                # Filtrer et trier les comptes rendus pour les dates passées
                past_comptes_rendus = [cr for cr in comptes_rendus if cr.date < current_date]
                past_comptes_rendus.sort(key=lambda page: page.date, reverse=True)
                # Sélectionner les éléments selon items_number
                convocations = future_convocations[:items_number]
                comptes_rendus = past_comptes_rendus[:items_number]
                # Ajout des éléments de la page actuelle pour la page soeur suivante
                update_cv_cr_list.previous_conv = convocations
                update_cv_cr_list.previous_cr = comptes_rendus                
                # Fusion des listes
                menu_items = convocations + comptes_rendus
                # print(colored(f'menu_items: {menu_items}', 'white', 'on_green'))

                
        elif type == 'menu':
            # print(colored("MENU", 'green'))            
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
            # print(colored("NAV", 'green'))
            # Trier tous ensemble
            if child == 'convocation':
                menu_items = sorted(convocations, key=lambda page: page.date, reverse=True)[:3]
            elif child == 'compte-rendu':   
                menu_items = sorted(comptes_rendus, key=lambda page: page.date, reverse=True)[:3]
                
    return menu_items