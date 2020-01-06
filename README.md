# ttss-client
Python script for searching public transport rides in Kraków, cli front for ttss.krakow.pl service

## Installation
Clone repository

`git clone https://github.com/fbiernat/ttss-client.git`

Change directory

`cd ttss-client`

Install dependencies

`pip3 install requests`

Run

`python3 ttss.py` or `./ttss`

## Sample output

```
   __  __               _________            __ 
  / /_/ /___________   / ____/ (_)__  ____  / /_
 / __/ __/ ___/ ___/  / /   / / / _ \/ __ \/ __/
/ /_/ /_(__  |__  )  / /___/ / /  __/ / / / /_  
\__/\__/____/____/   \____/_/_/\___/_/ /_/\__/  

WYSZUKIWARKA POŁĄCZEN KOMUNIKACJI MIEJSKIEJ W KRAKOWIE
Podaj nazwę przystanku początkowego mogil
Przystanek początkowy: Rondo Mogilskie
Podaj nazwę przystanku końcowego bagatel
Przystanek końcowy: Teatr Bagatela

      Rondo Mogilskie - Teatr Bagatela
==============================================
Odjazd wg Kierunek             Linia Odjazd za
rozkładu
----------------------------------------------
20:32     Bronowice Małe         4        0min
----------------------------------------------
20:34     Borek Fałęcki         19        1min
----------------------------------------------
20:37     Mistrzejowice          9        5min
----------------------------------------------
20:39     Kurdwanów P+R         50        5min
----------------------------------------------
20:40     Bronowice Małe        14        6min
----------------------------------------------
20:40     Mistrzejowice         14        6min
----------------------------------------------
20:41     Krowodrza Górka       50        7min
----------------------------------------------
20:42     Mały Płaszów P+R      20        9min
----------------------------------------------
20:44     Czerwone Maki P+R     52       10min
----------------------------------------------
20:38     Salwator              70       10min
----------------------------------------------
20:36     Krowodrza Górka        5       11min
----------------------------------------------
20:18     Salwator              70       11min
----------------------------------------------
20:45     Cichy Kącik           20       14min
----------------------------------------------
20:49     Nowy Bieżanów P+R      9       15min
----------------------------------------------
20:52     Bronowice Małe         4       18min
----------------------------------------------
20:54     Borek Fałęcki         19       20min
----------------------------------------------
20:56     Mistrzejowice          9       23min
----------------------------------------------
20:58     Krowodrza Górka       50       24min
----------------------------------------------
20:59     Kurdwanów P+R         50       25min
----------------------------------------------
21:00     Mistrzejowice         14       26min
----------------------------------------------
```
