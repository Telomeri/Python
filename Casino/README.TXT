# Kasino-Peli

## Ohjelmoin kasinopelin a+:ssa annettuja sääntöjä noudattaen, jonka aluksi tein tekstipohjaisena, ja näiden päälle rakensin
pyqt5:lla tehdyn graaffisenliittymän, jossa pääasiassa kommunikointi tapahtuu widgeteillä.

## Tiedosto- ja kansiorakenne

  - README-VALI.txt kohdasta löytyy välipalautuksen readme
  - Docs kohdan alta löytyy projektiin liittyvä dokumentointi
  - thoughts.txt sisältää ohjelmassa käytetyn yhden algoritmin hahmotelman
  - Kaikki koodit ovat omatekemääni, joita on muutettu monta kertaa projektin aikana, ja pyritty siistimään parhaan taitoni mukaan. 
  Lähes kaikki koodi sijoittuu GUI:ssa olevaan MainWindow classiin, joka johtuu kokemattomuudesta PyQt5:sen alaluokkien kanssa.
  Ohjelma kuitenkin hyödyntää vahvasti muita luokkia, tarvittavat osat ohjelmaa on määritelty.

## Asennusohje

  - Ohjelma tarvitsee ainoana kirjastona pyqt5, muut ohjelman käyttämät apuvälineet ovat sisäänrakennettuja
  - Pythonin omia kirjastoja käytössä:
  	sys, random ja functools

## Käyttöohje

  - Ohjelmaa pyöritetään main.py tiedostosta, ja se käynnistyy sitä suoritettaessa.
  - Ohjelma ei käytä mitään komentorivikomentoja, vaan kaikki tapahtuu puhtaasti suoraan graafisen liittymän kautta
  - Ohjelman suorittaessa ohjeet ovat selkeät. 
  1. Valitse ensin tapa jolla haluat aloittaa pelin
  2. Valitse pelaajien määrä
  3. Peli alkaa, ja päättyy kun joku pelaaja saa pelipisteitä 16.
  4. Pelin ohjeita voi seurata alhaalla olevasta tekstikentästä, ja korteista saa lisätietoa laittamalla hiiri niiden päälle.
Liike tehdään ensin painamalla korttia, jonka jälkeen valitaan halutut pöytäkortit, ja painetaan readynäppäintä
Vaihtoehtoinen liike on nostaa kortti, joka käyttää pelaajan vuoron. Tämä tapahtuu painamalla Draw Card näppäintä
Jos pöytä on täynnä, eli siinä on 12 korttia, kortteja ei voi nostaa. Jos pakka on tyhjä, kortteja ei voi nostaa,
mutta vuoro siirtyy näppäintä painamalla seuraavalle. Jos kukaan pelaajista ei voi tehdä liikettä 14 vuoroon, mutta 
pöydällä on vielä kortteja, kierros päättyy. Toinen tapa päättää kierros on jos pöydässä ja pakassa ei ole enää kortteja.
Pisteenlasku toimii samalla tavalla kuin ohjeissa.
  5. Ohjelman voi tallentaa ennalta-määrättyyn tiedostoon savegame näppäimellä, joka on nimellä savinggame.txt, valitettavasti en kerennyt tehdä
  loadgame versiota, joten kyseinen näppäin ei tee mitään.
  6. Kun peli päättyy, ohjelma on käynnissä, mutta mitään liikkeitä ei voi tehdä. Jos haluaa päättää pelin ennenaikaisesti, on se suljettava
  painamalla rastia. 