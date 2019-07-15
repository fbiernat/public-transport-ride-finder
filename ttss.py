import requests
import sys

# TODO: [-] dodanie przekazywania argumentów funkcji wyszukujących przystanki z linii poleceń
#		[ ] obsługa polskich znaków w odpowiedzi z serwera
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
        print('Przystanek ' + stopName + ' nie istnieje')
        return

    if count == 1:
        userInput = 1
    else:
        for i in range(1, count + 1):
            print(str(i) + ' - ' + res[i]['name'])

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
    stopName = res[userInput]['name']

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


def main():
    if (len(sys.argv) != 1 and len(sys.argv) != 3):
        print('Sposob użycia python3 ttss.py nazwa-przystanku-poczatkowego nazwa-przystanku-koncowego')
        return

    print('Wyszukiwarka polaczen komunikacji miejskiej w Krakowie'.upper())

    if (len(sys.argv) == 1):
        start = getStop(input('Podaj nazwe przystanku poczatkowego '))
        stop = getStop(input('Podaj nazwe przystanku koncowego '))
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

    print(getLine(37, '-'))

    # wyswietl odjazdy z przystanku poczatkowego
    if len(departures) == 0:
        print('Brak przejazdów')
    else:
        print('{} {:20} {}'.format('Planowany', 'Kierunek', 'Linia'))
        print('odjazd')

        print(getLine(37, '-'))

        for dep in departures:
            # print(dep)
            time = dep.get('actualTime', 'Brak')
            print('{:9} {:20} {:5}'.format(
                time, dep['direction'], dep['patternText']))

        print(getLine(37, '-'))


main()
