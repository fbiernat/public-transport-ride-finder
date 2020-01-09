import requests
import sys
from math import floor, ceil
from html import unescape

# TODO: [-] dodanie przekazywania argumentów funkcji wyszukujących przystanki z linii poleceń
#       [-] format czasu do odjazdu tramwaju (np <1min.)
#       [ ] rozwinięcie algorytmu wyszukiwania przejazdów (obsługa tras z przesiadkami)
#       [-] pobranie i wyświetlenie listy przystanków
#       [-] zapis i odczyt listy przystanków do/z pliku

API_URL = 'http://www.ttss.krakow.pl/internetservice/services/'


def getStopInfo(stopName):
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
            print(str(i) + ' - ' + unescape(res[i]['name']))

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
    stopName = unescape(res[userInput]['name'])

    return {'id': stopId, 'name': stopName}


def getDepartureInfo(stopId):
    departureRequestUrl = API_URL + \
        'passageInfo/stopPassages/stop?stop={}&mode=departure&language=en'.format(
            stopId)
    res = requests.get(departureRequestUrl)
    return res.json()


def printLine(length, character='-'):
    line = ''
    for i in range(length):
        line += character

    print(line)


def printMinutesToDeparture(seconds):
    if seconds == '-':
        return '-'

    if seconds >= 0:
        minutes = floor(seconds / 60)
        if minutes == 0:
            return '<1min'
    else:
        minutes = ceil(seconds / 60)

    return str(minutes) + 'min'


def printLogo():
    with open('logo.txt') as f:
        lines = f.readlines()
        for line in lines:
            print(line.rstrip('\n'))

    print('\nWyszukiwarka połączen komunikacji miejskiej w Krakowie'.upper())
    print('')


def listDepartures(start, stop, numberOfDepartures):
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

    trasa = '{:>21} - {}'.format(start['name'], stop['name'])
    print(trasa)

    printLine(lineLength, '=')

    if len(departures) == 0:
        print('Brak przejazdów')
        printLine(lineLength, '-')

    # wyswietl odjazdy z przystanku poczatkowego
    else:
        print('{:9} {:20} {:5} {}'.format(
            'Odjazd wg', 'Kierunek', 'Linia', 'Odjazd za'))
        print('rozkładu')

        printLine(lineLength, '-')
        i = 0
        for daparture in departures:
            i += 1
            time = daparture.get('plannedTime', 'Brak')
            relTimeSeconds = daparture.get('actualRelativeTime', '-')
            print('{:9} {:20} {:^5} {:>9}'.format(
                time, daparture['direction'], daparture['patternText'],
                printMinutesToDeparture(relTimeSeconds)))
            printLine(lineLength, '-')
            if i == numberOfDepartures:
                break


def printStops(inputString=None):
    if (inputString != None and len(inputString) >= 1):
        letters = []
        letters.append(inputString[0].upper())
    else:
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                   'o', 'p', 'r', 's', 't', 'u', 'w', 'z']
    stopList = []

    try:
        f = open('stops.txt', 'r')
        lines = f.readlines()
        for line in lines:
            if len(letters) == 1 and line[0] == letters[0][0]:
                stopList.append(line.strip())
        f.close()

    except FileNotFoundError:
        f = open('stops.txt', 'w')
        for letter in letters:
            requestURL = API_URL + \
                'lookup/stopsByCharacter?character={}&language=en'.format(
                    letter.upper())
            try:
                resp = requests.get(requestURL)
                stops = resp.json()['stops']
                for stop in stops:
                    stopName = stop['name']
                    stopList.append(stopName)
                    f.write(stopName + '\n')

            except Exception:
                print('Nie udało się nawiązać połączenia')
                break
        f.close()

    print('Lista przystanków:')
    for stop in stopList:
        print(stop)


def main():
    if (len(sys.argv) > 3):
        print('Sposob użycia:')
        print('python3 ttss.py nazwa-przystanku-poczatkowego nazwa-przystanku-koncowego')
        print('python3 ttss.py list')
        return

    printLogo()
    try:
        if len(sys.argv) == 1 or (len(sys.argv) == 3 and sys.argv[1] != 'list'):
            if len(sys.argv) == 1:
                start = getStopInfo(input('Podaj nazwę przystanku początkowego '))
                if start == None:
                    print('Nie podano przystanku')
                    return
                print('Przystanek początkowy: ' + start['name'])
                stop = getStopInfo(input('Podaj nazwę przystanku końcowego '))
                if stop == None:
                    print('Nie podano przystanku')
                    return
                print('Przystanek końcowy: ' + stop['name'])

            elif len(sys.argv) == 3:
                start = getStopInfo(sys.argv[1])
                stop = getStopInfo(sys.argv[2])

            if start != None and stop != None:
                if stop['id'] == start['id']:
                    print('Wybrano ten sam przystanek')
                    return

                listDepartures(start, stop, 15)

        elif len(sys.argv) == 2 and sys.argv[1] == 'list':
            # lista przystankow
            printStops()

        elif len(sys.argv) == 3 and sys.argv[1] == 'list':
            printStops(sys.argv[2])
    except KeyboardInterrupt:
        return

main()
