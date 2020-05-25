import re

from MySQLdb._exceptions import DataError
from django.core.management.base import BaseCommand, CommandError

from autocomplete.models import AutoComplete
from base.models import ServiceOrder


class Command(BaseCommand):
    help = 'Refresh info for ajax autocomplete'
    regexer=re.compile('[,\(\)]')

    def parse_ajax_texts(self, text):
        if text:
            if len(text)<150:
                results = [text]
            else:
                results = []
            if text.find(','):
                res = self.regexer.split(text)
                results.extend(elem.strip() for elem in res if elem and 4 < len(elem) < 150)
            return results
        else:
            return []

    def insert_variants(self, variants, section='CM'):
        if variants:
            for variant in variants:
                count = AutoComplete.objects.filter(section=section).filter(text=variant).count()
                if count == 0:
                    try:
                        ajax_search = AutoComplete(section=section, text=variant)
                        ajax_search.save()
                    except DataError:
                        print(variant)

    def process_varian(self, text, section='CM'):
        if text:
            result = self.parse_ajax_texts(text)
            #print(text, result)
            self.insert_variants(result, section=section)
            #print('INSERT '+str(len(result)))

    def handle(self, *args, **options):
        service_orders = ServiceOrder.objects.all()

        for service_order in service_orders:
            equipment = service_order.equipment
            demage = service_order.damage

            self.process_varian(equipment, section='CM')
            self.process_varian(demage, section='ER')