import requests
import time
import sys
from math import floor
import html

# TODO: [-] dodanie przekazywania argumentów funkcji wyszukujących przystanki z linii poleceń
#		[ ] format czasu do odjazdu tramwaju (np <1min.)
# 		[ ] rozwinięcie algorytmu wyszukiwania przejazdów (obsługa tras z przesiadkami)

url = 'http://www.ttss.krakow.pl/internetservice/services/'


# curl http://www.ttss.krakow.pl/internetservice/services/lookup/autocomplete/json?query=123&language=en
def getStop(stopName):
    stopQueryUrl = url + 'lookup/autocomplete/json?query={}&language=en'
    r = requests.get(stopQueryUrl.format(stopName))
    res = r.json()

    try:
        if res == []:
            raise IndexError
        count = r.json()[0]['count']
    except IndexError:
        print('Nie znaleziono przystanku ' + stopName)
        return 0

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
    departureRequestUrl = url + \
        'passageInfo/stopPassages/stop?stop={}&mode=departure&language=en'.format(
            stopId)
    res = requests.get(departureRequestUrl)
    return res.json()


def getLine(length, character):
    line = ''
    for i in range(length):
        line += character

    return line


def compareTime(time1, time2):
    # print(time1 + ', ' + time2)
    result = ''
    deltaH = 0
    if time2 == 'Brak':
        return 'Brak'

    t1 = time1.split(':')
    t2 = time2.split(':')

    t1[0] = int(t1[0])
    t2[0] = int(t2[0])
    t1[1] = int(t1[1])
    t2[1] = int(t2[1])

    if t1[0] >= t2[0] and t1[1] >= t2[1]:
        return 'Odjechał'

    if t1[0] < t2[0]:
        deltaH = t2[0] - t1[0]
        t2[1] += 60 * deltaH
        # result += str(t2[0] - t1[0]) + 'h'

    if t1[1] < t2[1]:
        delta = t2[1] - t1[1]
        if delta == 0:
            return 'Odjechał'
        else:
            if deltaH > 0:
                delta += deltaH * 60
            if delta >= 60:
                hours = floor(delta / 60)
                if hours > 1:
                    result += str(hours) + 'h'
                delta -= hours * 60
            result += str(delta) + 'min'

    return result


def main():
    if (len(sys.argv) != 1 and len(sys.argv) != 3):
        print('Sposob użycia python3 ttss.py nazwa-przystanku-poczatkowego nazwa-przystanku-koncowego')
        return

    with open('logo.txt') as l:
        lines = l.readlines()
        for line in lines:
            print(line.rstrip('\n'))

    print('\nWyszukiwarka polaczen komunikacji miejskiej w Krakowie'.upper())

    if (len(sys.argv) == 1):
        try:
            while True:
                start = getStop(input('Podaj nazwe przystanku poczatkowego '))
                if start != 0:
                    break

            print('START: ' + start['name'])
            while True:
                stop = getStop(input('Podaj nazwe przystanku koncowego '))
                if stop != 0:
                    break
            print('STOP: ' + stop['name'])
        except KeyboardInterrupt:
            print()
            return
    else:
        if len(sys.argv) == 3:
            start = getStop(sys.argv[1])
            stop = getStop(sys.argv[2])

    if start == None or stop == None:
        print('Brak danych, sproboj jeszcze raz')
        return

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

    global time
    localtime = time.localtime(time.time())
    hourNow = localtime.tm_hour
    minutesNow = localtime.tm_min
    timeNow = str(hourNow) + ':' + str(minutesNow)

    # wyswietl odjazdy z przystanku poczatkowego
    if len(departures) == 0:
        print('Brak przejazdów')
    else:
        print('{} {:^20} {:5} {}'.format(
            'Odjazd wg', 'Kierunek', 'Linia', 'Odjazd za'))
        print('rozkladu')

        print(getLine(lineLength, '-'))

        for dep in departures:
            # print(dep)
            time = dep.get('plannedTime', 'Brak')
            print('{:9} {:20} {:5} {}'.format(
                time, dep['direction'], dep['patternText'], compareTime(timeNow, time)))

        print(getLine(lineLength, '-'))


main()
