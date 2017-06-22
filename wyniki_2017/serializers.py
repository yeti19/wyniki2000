from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from wyniki_2017.models import *


class VoivodeshipSerializer(ModelSerializer):
    class Meta:
        model = Voivodeship
        exclude = ['num']


class DistrictSerializer(ModelSerializer):
    class Meta:
        model = District
        exclude = ['num']
        extra_kwargs = {'name': {'required': False}}


class CommuneSerializer(ModelSerializer):
    class Meta:
        model = Commune
        exclude = ['num']
        extra_kwargs = {'name': {'required': False}}


class PrecinctSerializer(ModelSerializer):
    class Meta:
        model = Precinct
        exclude = ['id', 'num', 'allowed', 'cards_issued', 'votes_cast', 'valid_votes', 'invalid_votes']
        extra_kwargs = {'name': {'required': False},
                        'address': {'required': False},
                        'commune': {'required': False},
                        'votes_1': {'required': False},
                        'votes_2': {'required': False},
                        'votes_3': {'required': False},
                        'votes_4': {'required': False},
                        'votes_5': {'required': False},
                        'votes_6': {'required': False},
                        'votes_7': {'required': False},
                        'votes_8': {'required': False},
                        'votes_9': {'required': False},
                        'votes_10': {'required': False},
                        'votes_11': {'required': False},
                        'votes_12': {'required': False}}