from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.forms import ModelForm
from django.core.exceptions import ValidationError


def get_data(a):
    total = [a['allowed'], a['cards_issued'], a['votes_cast'],
             a['invalid_votes'], a['valid_votes'], a['votes_1'],
             a['votes_2'], a['votes_3'], a['votes_4'], a['votes_5'],
             a['votes_6'], a['votes_7'], a['votes_8'], a['votes_9'],
             a['votes_10'], a['votes_11'], a['votes_12']]
    return total


def aggregate_precincts(objects):
    a = objects.aggregate(allowed=Coalesce(Sum('allowed'), 0),
                          cards_issued=Coalesce(Sum('cards_issued'), 0),
                          votes_cast=Coalesce(Sum('votes_cast'), 0),
                          invalid_votes=Coalesce(Sum('invalid_votes'), 0),
                          valid_votes=Coalesce(Sum('valid_votes'), 0),
                          votes_1=Coalesce(Sum('votes_1'), 0),
                          votes_2=Coalesce(Sum('votes_2'), 0),
                          votes_3=Coalesce(Sum('votes_3'), 0),
                          votes_4=Coalesce(Sum('votes_4'), 0),
                          votes_5=Coalesce(Sum('votes_5'), 0),
                          votes_6=Coalesce(Sum('votes_6'), 0),
                          votes_7=Coalesce(Sum('votes_7'), 0),
                          votes_8=Coalesce(Sum('votes_8'), 0),
                          votes_9=Coalesce(Sum('votes_9'), 0),
                          votes_10=Coalesce(Sum('votes_10'), 0),
                          votes_11=Coalesce(Sum('votes_11'), 0),
                          votes_12=Coalesce(Sum('votes_12'), 0))
    return get_data(a)


# Kraj > województwo > okręg > gmina > obwody
class Voivodeship(models.Model):
    name = models.CharField(max_length=32)
    num = models.AutoField(primary_key=True)

    def aggregate_precincts(self):
        return aggregate_precincts(Precinct.objects.filter(
                                   commune__district__voivodeship=self))

    def save(self, *args, **kwargs):
        if self.num is None and 'num' not in kwargs:
            try: self.num = Voivodeship.objects.all().order_by('num').last().num + 1
            except: self.num = 0
        return super(Voivodeship, self).save(*args, **kwargs)


class District(models.Model):
    name = models.CharField(max_length=32)
    num = models.PositiveIntegerField(primary_key=True)
    voivodeship = models.ForeignKey(Voivodeship, on_delete=models.SET_NULL, null=True)

    def aggregate_precincts(self):
        return aggregate_precincts(Precinct.objects.filter(commune__district=self))

    def save(self, *args, **kwargs):
        if self.num is None and 'num' not in kwargs:
            try: self.num = District.objects.all().order_by('num').last().num + 1
            except: self.num = 0
        return super(District, self).save(*args, **kwargs)


class Commune(models.Model):
    name = models.CharField(max_length=32)
    num = models.PositiveIntegerField(primary_key=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)

    def aggregate_precincts(self):
        return aggregate_precincts(Precinct.objects.filter(commune=self))

    def save(self, *args, **kwargs):
        if self.num is None and 'num' not in kwargs:
            try: self.num = Commune.objects.all().order_by('num').last().num + 1
            except: self.num = 0
        return super(Commune, self).save(*args, **kwargs)


class Precinct(models.Model):
    num = models.PositiveIntegerField(default=0, verbose_name='Numer obwodu w gminie')
    address = models.CharField(max_length=64, verbose_name='Adres obwodu')
    commune = models.ForeignKey(Commune, on_delete=models.SET_NULL, null=True)
    allowed = models.PositiveIntegerField(default=0, verbose_name='Dopuszczeni do głosowania')
    cards_issued = models.PositiveIntegerField(default=0, verbose_name='Karty wydane')
    votes_cast = models.PositiveIntegerField(default=0, verbose_name='Oddane głosy')
    valid_votes = models.PositiveIntegerField(default=0, verbose_name='Ważne głosy')
    invalid_votes = models.PositiveIntegerField(default=0, verbose_name='Nieważne głosy')
    votes_1 = models.PositiveIntegerField(default=0, verbose_name='Grabowski Dariusz Maciej')
    votes_2 = models.PositiveIntegerField(default=0, verbose_name='Ikonowicz Piotr')
    votes_3 = models.PositiveIntegerField(default=0, verbose_name='Kalinowski Jarosław')
    votes_4 = models.PositiveIntegerField(default=0, verbose_name='Korwin - Mikke Janusz')
    votes_5 = models.PositiveIntegerField(default=0, verbose_name='Krzaklewski Marian')
    votes_6 = models.PositiveIntegerField(default=0, verbose_name='Kwaśniewski Aleksander')
    votes_7 = models.PositiveIntegerField(default=0, verbose_name='Lepper Andrzej')
    votes_8 = models.PositiveIntegerField(default=0, verbose_name='Łopuszański Jan')
    votes_9 = models.PositiveIntegerField(default=0, verbose_name='Olechowski Andrzej Marian')
    votes_10 = models.PositiveIntegerField(default=0, verbose_name='Pawłowski Bogdan')
    votes_11 = models.PositiveIntegerField(default=0, verbose_name='Wałęsa Lech')
    votes_12 = models.PositiveIntegerField(default=0, verbose_name='Wilecki Tadeusz Adam')

    def aggregate_precincts(self):
        return get_data(self.__dict__)

    def clean(self):
        sum_votes = self.votes_1 + self.votes_2 + self.votes_3 + self.votes_4 +\
                    self.votes_5 + self.votes_6 + self.votes_7 + self.votes_8 +\
                    self.votes_9 + self.votes_10 + self.votes_11 + self.votes_12
        if sum_votes != self.valid_votes:
            raise ValidationError({
                'valid_votes': 'Głosy nie sumują się do \'ważne głosy\'.'})
        if self.valid_votes + self.invalid_votes != self.votes_cast:
            raise ValidationError({
                'votes_cast': 'Głosy ważne i nieważne nie sumują się do \'oddane głosy\'.'})
        if self.votes_cast > self.cards_issued:
            raise ValidationError({
                'cards_issued': 'Wydano mniej kart niż oddanych głosów.'})
        if self.cards_issued > self.allowed:
            raise ValidationError({
                'allowed': 'Wydano więcej kart niż było uprawnionych do głosowania.'})
