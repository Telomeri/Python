# Kasino-Peli

## Ohjelmoin kasinopelin a+:ssa annettuja s��nt�j� noudattaen, jonka aluksi tein tekstipohjaisena, ja n�iden p��lle rakensin
pyqt5:lla tehdyn graaffisenliittym�n, jossa p��asiassa kommunikointi tapahtuu widgeteill�.

## Tiedosto- ja kansiorakenne

  - README-VALI.txt kohdasta l�ytyy v�lipalautuksen readme
  - Docs kohdan alta l�ytyy projektiin liittyv� dokumentointi
  - thoughts.txt sis�lt�� ohjelmassa k�ytetyn yhden algoritmin hahmotelman
  - Kaikki koodit ovat omatekem��ni, joita on muutettu monta kertaa projektin aikana, ja pyritty siistim��n parhaan taitoni mukaan. 
  L�hes kaikki koodi sijoittuu GUI:ssa olevaan MainWindow classiin, joka johtuu kokemattomuudesta PyQt5:sen alaluokkien kanssa.
  Ohjelma kuitenkin hy�dynt�� vahvasti muita luokkia, tarvittavat osat ohjelmaa on m��ritelty.

## Asennusohje

  - Ohjelma tarvitsee ainoana kirjastona pyqt5, muut ohjelman k�ytt�m�t apuv�lineet ovat sis��nrakennettuja
  - Pythonin omia kirjastoja k�yt�ss�:
  	sys, random ja functools

## K�ytt�ohje

  - Ohjelmaa py�ritet��n main.py tiedostosta, ja se k�ynnistyy sit� suoritettaessa.
  - Ohjelma ei k�yt� mit��n komentorivikomentoja, vaan kaikki tapahtuu puhtaasti suoraan graafisen liittym�n kautta
  - Ohjelman suorittaessa ohjeet ovat selke�t. 
  1. Valitse ensin tapa jolla haluat aloittaa pelin
  2. Valitse pelaajien m��r�
  3. Peli alkaa, ja p��ttyy kun joku pelaaja saa pelipisteit� 16.
  4. Pelin ohjeita voi seurata alhaalla olevasta tekstikent�st�, ja korteista saa lis�tietoa laittamalla hiiri niiden p��lle.
Liike tehd��n ensin painamalla korttia, jonka j�lkeen valitaan halutut p�yt�kortit, ja painetaan readyn�pp�int�
Vaihtoehtoinen liike on nostaa kortti, joka k�ytt�� pelaajan vuoron. T�m� tapahtuu painamalla Draw Card n�pp�int�
Jos p�yt� on t�ynn�, eli siin� on 12 korttia, kortteja ei voi nostaa. Jos pakka on tyhj�, kortteja ei voi nostaa,
mutta vuoro siirtyy n�pp�int� painamalla seuraavalle. Jos kukaan pelaajista ei voi tehd� liikett� 14 vuoroon, mutta 
p�yd�ll� on viel� kortteja, kierros p��ttyy. Toinen tapa p��tt�� kierros on jos p�yd�ss� ja pakassa ei ole en�� kortteja.
Pisteenlasku toimii samalla tavalla kuin ohjeissa.
  5. Ohjelman voi tallentaa ennalta-m��r�ttyyn tiedostoon savegame n�pp�imell�, joka on nimell� savinggame.txt, valitettavasti en kerennyt tehd�
  loadgame versiota, joten kyseinen n�pp�in ei tee mit��n.
  6. Kun peli p��ttyy, ohjelma on k�ynniss�, mutta mit��n liikkeit� ei voi tehd�. Jos haluaa p��tt�� pelin ennenaikaisesti, on se suljettava
  painamalla rastia. 