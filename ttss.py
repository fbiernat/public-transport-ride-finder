import requests
import time
import sys
from math import floor, ceil
import html

# TODO: [-] dodanie przekazywania argumentów funkcji wyszukujących przystanki z linii poleceń
#       [-] format czasu do odjazdu tramwaju (np <1min.)
#       [ ] rozwinięcie algorytmu wyszukiwania przejazdów (obsługa tras z przesiadkami)

API_URL = 'http://www.ttss.krakow.pl/internetservice/services/'

# curl http://www.ttss.krakow.pl/internetservice/services/lookup/autocomplete/json?query=123&language=en


def getStop(stopName):
    if not stopName:
        return None

    try:
        stopQueryURL = API_URL + 'lookup/autocomplete/json?query={}&language=en'
        r = requests.get(stopQueryURL.format(stopName))
        res = r.json()
        if res == []:
            raise IndexError
        count = r.json()[0]['count']
    except IndexError:
        print('Nie znaleziono przystanku ' + stopName)
        return None
    except Exception:
        print('Nie udało się nawiązać połączenia')

    if count == 1:
        userInput = 1
    else:
        for i in range(1, count + 1):
            print(str(i) + ' - ' + html.unescape(res[i]['name']))

        while True:
            userInput = input('Wybierz numer przystanku ')
            try:
                userInput = int(userInput)
                if userInput < 0 or userInput > count:
                    raise ValueError
            except ValueError:
                print('Podaj liczbe z zakresu 1 - ' + count)
                continue
            break

    stopId = res[userInput]['id']
    stopName = html.unescape(res[userInput]['name'])

    return {'id': stopId, 'name': stopName}

# curl http://www.ttss.krakow.pl/internetservice/services/passageInfo/stopPassages/stop?stop=125&mode=departure&language=en


def getDepartureInfo(stopId):
    departureRequestUrl = API_URL + \
        'passageInfo/stopPassages/stop?stop={}&mode=departure&language=en'.format(
            stopId)
    res = requests.get(departureRequestUrl)
    return res.json()


def getLine(length, character):
    line = ''
    for i in range(length):
        line += character

    return line


def printMinutesToDeparture(seconds):
    if seconds == '-':
        return seconds

    if seconds >= 0:
        minutes = floor(seconds / 60)
        if minutes == 0:
            return '<1min'
    else:
        minutes = ceil(seconds / 60)
        if minutes == 0:
            return '-'

    return str(minutes) + 'min'


def printLogo():
    with open('logo.txt') as l:
        lines = l.readlines()
        for line in lines:
            print(line.rstrip('\n'))

    print('\nWyszukiwarka polaczen komunikacji miejskiej w Krakowie'.upper())


def main():
    if (len(sys.argv) != 1 and len(sys.argv) != 3):
        print('Sposob użycia python3 ttss.py nazwa-przystanku-poczatkowego nazwa-przystanku-koncowego')
        return

    # print logo
    printLogo()

    if len(sys.argv) == 1:
        start = getStop(input('Podaj nazwe przystanku poczatkowego '))
        if start == None:
            print('Nie podano przystanku')
            return
        print('START: ' + start['name'])
        stop = getStop(input('Podaj nazwe przystanku koncowego '))
        if stop == None:
            print('Nie podano przystanku')
            return
        print('STOP: ' + stop['name'])

    elif len(sys.argv) == 3:
        start = getStop(sys.argv[1])
        stop = getStop(sys.argv[2])

    if stop['id'] == start['id']:
        print('Wybrano ten sam przystanek')
        return

    if start == None or stop == None:
        print('Brak danych, sproboj jeszcze raz')
        return

    print()
    trasa = '{} - {}'.format(start['name'], stop['name'])
    print(trasa)

    # pobierz trasy przystanku koncowego
    directions = []
    for route in getDepartureInfo(stop['id'])['routes']:
        for direction in route['directions']:
            directions.append(direction)

    # szukaj lini o takich samych trasach wsrod lini przejezdzajacych przez przystanek poczatkowy
    departures = []
    for line in getDepartureInfo(start['id'])['actual']:
        if line['direction'] in directions:
            departures.append(line)

    lineLength = 46
    print(getLine(lineLength, '-'))

    if len(departures) == 0:
        print('Brak przejazdów')
        print(getLine(lineLength, '-'))

    # wyswietl odjazdy z przystanku poczatkowego
    else:
        print('{} {:20} {:5} {}'.format(
            'Odjazd wg', 'Kierunek', 'Linia', 'Odjazd za'))
        print('rozkladu')

        print(getLine(lineLength, '-'))

        for daparture in departures:
            time = daparture.get('plannedTime', 'Brak')
            relTimeSeconds = daparture.get('actualRelativeTime', '-')
            print('{:9} {:20} {:5} {}'.format(
                time, daparture['direction'], daparture['patternText'],
                printMinutesToDeparture(relTimeSeconds)))

            print(getLine(lineLength, '-'))


main()
