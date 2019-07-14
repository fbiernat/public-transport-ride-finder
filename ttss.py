import requests

def getStop(stopName):
	stopQuery = 'http://www.ttss.krakow.pl/internetservice/services/lookup/autocomplete/json?query={}&language=en'
	r = requests.get(stopQuery.format(stopName))
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

print('Wyszukiwarka polaczen komunikacji miejskiej')
start = getStop(input('Podaj nazwe przystanku poczatkowego '))
stop = getStop(input('Podaj nazwe przystanku koncowego '))

if start == None or stop == None:
	print('Brak danych, sproboj jeszcze raz')

