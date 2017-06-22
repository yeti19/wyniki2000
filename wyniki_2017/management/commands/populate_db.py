from xlrd import open_workbook
import os
from wyniki_2017.models import *
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = ''
    help = 'Wczytuje dane wyborów do bazy danych'

    def handle(self, *args, **options):
        dirpath = os.path.dirname(os.path.dirname(__file__)) + '/data/'
        sheet = open_workbook(dirpath + 'zal2.xls').sheet_by_index(0)

        ds = []
        cs = []

        last = None
        for i in range(sheet.nrows):
            if sheet.cell(i, 0).value == 'województwo':
                last = Voivodeship(name=sheet.cell(i, 1).value.title())
                last.save()
            elif last:
                ds.append(District(name=sheet.cell(i, 1).value,
                                   num=int(sheet.cell(i, 0).value),
                                   voivodeship=last))
                ds[-1].save()

        for okręg in range(1, 69):
            filename = dirpath + 'obw/obw' + str(okręg).zfill(2) + '.xls'
            sheet = open_workbook(filename).sheet_by_index(0)

            for j in range(1, sheet.nrows):
                if len(cs) == 0 or int(sheet.cell(j, 1).value) != cs[-1].num:
                    cs.append(Commune(name=sheet.cell(j, 2).value,
                                      num=int(sheet.cell(j, 1).value),
                                      district=ds[okręg - 1]))
                    cs[-1].save()

                p = Precinct(num=int(sheet.cell(j, 4).value),
                             address=sheet.cell(j, 6).value,
                             commune=cs[-1],
                             allowed=int(sheet.cell(j, 7).value),
                             cards_issued=int(sheet.cell(j, 8).value),
                             votes_cast=int(sheet.cell(j, 9).value),
                             invalid_votes=int(sheet.cell(j, 10).value),
                             valid_votes=int(sheet.cell(j, 11).value),
                             votes_1=int(sheet.cell(j, 12).value),
                             votes_2=int(sheet.cell(j, 13).value),
                             votes_3=int(sheet.cell(j, 14).value),
                             votes_4=int(sheet.cell(j, 15).value),
                             votes_5=int(sheet.cell(j, 16).value),
                             votes_6=int(sheet.cell(j, 17).value),
                             votes_7=int(sheet.cell(j, 18).value),
                             votes_8=int(sheet.cell(j, 19).value),
                             votes_9=int(sheet.cell(j, 20).value),
                             votes_10=int(sheet.cell(j, 21).value),
                             votes_11=int(sheet.cell(j, 22).value),
                             votes_12=int(sheet.cell(j, 23).value))
                p.save()
