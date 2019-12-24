# ttss-client
```
   __  __               _________            __ 
  / /_/ /___________   / ____/ (_)__  ____  / /_
 / __/ __/ ___/ ___/  / /   / / / _ \/ __ \/ __/
/ /_/ /_(__  |__  )  / /___/ / /  __/ / / / /_  
\__/\__/____/____/   \____/_/_/\___/_/ /_/\__/  
```
Python script for searching public transport rides in Kraków, cli front for ttss.krakow.pl service

## Installation
Clone repository

`git clone https://github.com/fbiernat/ttss-client.git`

Change directory

`cd ttss-client`

Install dependencies

`pip3 install requests`

Run

`python3 ttss.py`

Sample input

```
python3 ttss.py bagatela mogilskie
		    ^        ^
		    |        |____ destination stop
		    |	            
		    |_____________ starting stop
```
