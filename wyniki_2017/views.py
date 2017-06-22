from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from wyniki_2017.models import *
from wyniki_2017.serializers import *
from django.shortcuts import render

candidate_names = [
    'Grabowski Dariusz Maciej',
    'Ikonowicz Piotr',
    'Kalinowski Jarosław',
    'Korwin - Mikke Janusz',
    'Krzaklewski Marian',
    'Kwaśniewski Aleksander',
    'Lepper Andrzej',
    'Łopuszański Jan',
    'Olechowski Andrzej Marian',
    'Pawłowski Bogdan',
    'Wałęsa Lech',
    'Wilecki Tadeusz Adam',
]

def JsonResponseWithUser(request, variables):
    variables['user'] = request.user.username
    return JsonResponse(variables)


def make_candidates(total):
    candidates = []
    for i in range(len(candidate_names)):
        if total[2] == 0:
            percents = '0.0%'
        else:
            percents = '{0:.2f}%'.format(total[5 + i] / total[2] * 100.0)
        candidates.append({
            'n': i,
            'name': candidate_names[i],
            'votes': total[5 + i],
            'votes_percent': percents,
            'color': 'red',
        })
    return candidates


def put_request(request, SerializerClass, this=None):
    if not request.user.is_authenticated():
        return JsonResponseWithUser(request, {'result': 'Niezalogowani użytkownicy nie mogą edytować.'})
        
    data = JSONParser().parse(request)
    serializer = SerializerClass(this, data=data) if this else SerializerClass(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponseWithUser(request, {'result': 'success'})
    else:
        return JsonResponseWithUser(request, {'result': repr(serializer.errors) })


def delete_request(request, this):
    if not request.user.is_authenticated():
        return JsonResponseWithUser(request, {'result': 'Niezalogowani użytkownicy nie mogą usuwać.'})

    if this.delete()[0] == 1:
        return JsonResponseWithUser(request, {'result': 'success'})
    else:
        return JsonResponseWithUser(request, {'result': 'failure'})


def country(request):
    total = aggregate_precincts(Precinct.objects)
    regions = []
    for w in Voivodeship.objects.all():
        tot = w.aggregate_precincts()
        regions.append({'n': w.num, 'name': w.name,
                        'total': tot[2], 'candidate_votes': tot[5:5 + 12]})
    variables = {'candidates': make_candidates(total), 'regions': regions,
                 'make_map': True, 'down': '/woj/'}
    return JsonResponseWithUser(request, variables)

    
def commune(request, c=None):
    this = Commune.objects.get(num=c) if c else None

    if request.method == 'PUT':
        return put_request(request, CommuneSerializer, this)
    if request.method == 'DELETE':
        return delete_request(request, this)

    total = this.aggregate_precincts()
    regions = []
    for w in Precinct.objects.filter(commune__num=c):
        tot = w.aggregate_precincts()
        regions.append({'n': w.id, 'name': w.address,
                        'total': tot[2], 'candidate_votes': tot[5:5 + 12] })
    dangling = []
    for w in Precinct.objects.filter(commune__isnull=True):
        tot = w.aggregate_precincts()
        dangling.append({'n': w.id, 'name': w.address,
                        'total': tot[2], 'candidate_votes': tot[5:5 + 12] })
    variables = {'candidates': make_candidates(total), 'regions': regions, 'dangling': dangling,
                 'back': str(this.district.num), 'down': '/obwod/'}
    return JsonResponseWithUser(request, variables)


def district(request, d=None):
    this = District.objects.get(num=d) if d else None

    if request.method == 'PUT':
        return put_request(request, DistrictSerializer, this)
    if request.method == 'DELETE':
        return delete_request(request, this)

    total = this.aggregate_precincts()

    regions = []
    for w in Commune.objects.filter(district__num=d):
        tot = w.aggregate_precincts()
        regions.append({'n': w.num, 'name': w.name,
                        'total': tot[2], 'candidate_votes': tot[5:5 + 12]})

    dangling = []
    for w in Commune.objects.filter(district__isnull=True):
        tot = w.aggregate_precincts()
        dangling.append({'n': w.num, 'name': w.name,
                        'total': tot[2], 'candidate_votes': tot[5:5 + 12] })

    variables = {'candidates': make_candidates(total),
                 'regions': regions, 'dangling': dangling,
                 'back': str(this.voivodeship.num), 'down': '/gmina/'}
    return JsonResponseWithUser(request, variables)


def voivodeship(request, v=None):
    this = Voivodeship.objects.get(num=v) if v else None

    if request.method == 'PUT':
        return put_request(request, VoivodeshipSerializer, this)
    if request.method == 'DELETE':
        return delete_request(request, this)
    
    total = this.aggregate_precincts()

    regions = []
    for w in District.objects.filter(voivodeship__num=v):
        tot = w.aggregate_precincts()
        regions.append({'n': w.num, 'name': w.name,
                        'total': tot[2], 'candidate_votes': tot[5:5 + 12]})

    dangling = []
    for w in District.objects.filter(voivodeship__isnull=True):
        tot = w.aggregate_precincts()
        dangling.append({'n': w.num, 'name': w.name,
                        'total': tot[2], 'candidate_votes': tot[5:5 + 12] })

    variables = {'candidates': make_candidates(total), 'dangling': dangling,
                 'regions': regions, 'back': '0', 'down': '/okrag/'}
    return JsonResponseWithUser(request, variables)


def precinct(request, p=None):
    this = Precinct.objects.get(id=p) if p else None

    if request.method == 'PUT':
        return put_request(request, PrecinctSerializer, this)
    if request.method == 'DELETE':
        return delete_request(request, this)
    
    serializer = PrecinctSerializer(precinct)
    return JsonResponseWithUser(request, serializer.data)


def search(request):
    if not request.method == 'GET' or 'q' not in request.GET or 'type' not in request.GET:
        return JsonResponseWithUser(request, {'result': 'Błąd serwera. Nieprawidłowe zapytanie.'})

    q = request.GET['q']
    type = request.GET['type']

    if type == 'woj':
        ObjectsClass = Voivodeship
    elif type == 'okrag':
        ObjectsClass = District
    elif type == 'gmina':
        ObjectsClass = Commune
    elif type == 'obwod':
        ObjectsClass = Precinct
    else:
        return JsonResponseWithUser(request, {'result': 'Błąd serwera. Nieprawidłowe zapytanie.'})

    if type == 'obwod':
        objects = ObjectsClass.objects.filter(address__contains=q)
    else:
        objects = ObjectsClass.objects.filter(name__contains=q)

    if objects.count() == 0:
        return JsonResponseWithUser(request, {'result': 'Brak wyników wyszukiwania.'})

    total = [ 0 ] * 17
    regions = []
    for w in objects:
        tot = w.aggregate_precincts()
        if type == 'obwod':
            regions.append({'n': w.id, 'name': w.address,
                            'total': tot[2], 'candidate_votes': tot[5:5 + 12]})
        else:
            regions.append({'n': w.num, 'name': w.name,
                            'total': tot[2], 'candidate_votes': tot[5:5 + 12]})
        total = [ tot[i] + total[i] for i in range(17) ]
    variables = {'candidates': make_candidates(total),
                 'regions': regions, 'back': '0', 'down': '/gmina/'}
    return JsonResponseWithUser(request, variables)


    
def auth_login(request):
    data = JSONParser().parse(request)
    username = data['username']
    password = data['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponseWithUser(request, {'result': 'success'})
    return JsonResponseWithUser(request, {'result': 'failure'})

    
def auth_logout(request):
    if not request.user.is_authenticated():
        return JsonResponseWithUser(request, {'result': 'failure'})
    logout(request)
    return JsonResponseWithUser(request, {'result': 'success'})

    
def auth_register(request):
    data = JSONParser().parse(request)
    username = data['username']
    password = data['password']
    if authenticate(username=username, password=password) is not None:
        return JsonResponseWithUser(request, {'result': 'failure'})
    User.objects.create_user(username, password=password)
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponseWithUser(request, {'result': 'success'})
    return JsonResponseWithUser(request, {'result': 'failure'})
