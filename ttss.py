# TODO: * dodanie przekazywania argumentów funkcji wyszukujących przystanki z linii poleceń 
# 		* rozwinięcie algorytmu wyszukiwania przejazdów
#		* obsługa polskich znaków w odpowiedzi z serwera
#		* format czasu do odjazdu tramwaju (np <1min.)


import requests


url = 'http://www.ttss.krakow.pl/internetservice/services/'

def getStop(stopName):
	stopQueryUrl = url + 'lookup/autocomplete/json?query={}&language=en'
	r = requests.get(stopQueryUrl.format(stopName))
	res = r.json()
	try:
		count = r.json()[0]['count']
	except IndexError:
		print('Przystanek nie istnieje')
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

	# print(stopId + ' ' + stopName)

	return {'id': stopId, 'name': stopName}


def getDepartureInfo(stopId):
	departureRequestUrl = url + 'passageInfo/stopPassages/stop?stop={}&mode=departure&language=en'.format(stopId)
	res = requests.get(departureRequestUrl)
	return res.json()


print('Wyszukiwarka polaczen komunikacji miejskiej w Krakowie')
start = getStop(input('Podaj nazwe przystanku poczatkowego '))
stop = getStop(input('Podaj nazwe przystanku koncowego '))

if start == None or stop == None:
	print('Brak danych, sproboj jeszcze raz')

trasa = 'Trasa: {} - {}'.format(start['name'], stop['name'])
print(trasa)



# wez routes przystanku koncowego
directions = []
for route in getDepartureInfo(stop['id'])['routes']:
	for direction in route['directions']:
		directions.append(direction)

# szukaj lini o takich samych routes wsrod lini przejezdzajacych przez przystanek poczatkowy
departures = []
for line in getDepartureInfo(start['id'])['actual']:
	if line['direction'] in directions:
		departures.append(line)

# wyswietl odjazdy
for dep in departures:
	print('Linia {} kierunek {} odjazd {}'.format(dep['patternText'], dep['direction'], dep['actualTime']))

if len(departures) == 0:
	print('Brak przejazdów')
