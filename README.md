# lemmikkisovellus

## Lemmikkisovelluksella on tällä hetkellä seuraavat ominaisuudet:
1. Käyttäjä pystyyy tallentamaan lemmikkien tietoja. Lemmikin tiedoissa lukee sen eläinlaji, nimi, rotu, aktiivisuustaso ja ruokahalu. Aktiivisuustaso ja ruokahalu valitaan valmiista luokista.
2. Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen ja ulos siitä.
3. Käyttäjä näkee sovellukseen lisätyt lemmikit.
4. Käyttäjä pystyy lisäämään lemmikkejä ja muokkaamaan niiden tietoja ja poistamaan niitä (muokkaus ja poistaminen on mahdollista vain käyttäjän lisäämille lemmikeille).
5. Käyttäjä näkee lemmikkien tietoihin jätetyt kommentit
6. Käyttäjä pystyy kommentoimaan lemmikkejä, muokkaamaan kommenttia ja poistamaan niitä (muokkaus ja poistaminen on mahdollista vain käyttäjän lisäämille kommenteille).
7. Käyttäjä pystyy etsimään kommentteja hakusanalla. Haku hakee tällä hetkellä vain lemmikkien kommenteista.
8. käyttäjän sivuilta näkee kootusti käyttäjän lisäämät lemmikit ja kommentit.
9. Käyttäjä pystyy lisäämään kuvan itselleen käyttäjätietoihin, vaihtamaan sen ja poistamaan kuvan.
10. Käyttäjä pystyy lisäämään kuvan lisäämilleen lemmikeille, vaihtamaan ja poistamaan kuvan.
11. Käyttäjä pystyy arvostelemaan lemmikeitä (arvosanat 1-5), muokkaamaan ja poistamaan arvosteluja.
12. Lemmikin sivuilla näytetään tilastoja lemmikin arvosteluista.

Tässä pääasiallinen tietokohde on lemmikki ja toissijaisia tietokohteita ovat lemmikkien kommentit ja arvostelut.

## Yleistä toteutuksesta:

Sovelluksen tietokannan saat luotua schema.sql tiedoston avulla. Lisäksi sovelluksen git-kansiosta löytyy templates-kansiosta käytetyt html-sivupohjat ja sovelluksen käyttämät py-tiedostot. petinfo.py -tiedostossa on toteutettu kaikki metodit, joissa määritellään pet, messages ja grades -tauluihin liittyvät SQL-kyselyt. Users-tauluun liittyville sql-kyselyille on oma users.py -tiedosto. 

## Testausohjeet:

1. Aloita testaaminen kloonaamalla git-repositorio tietokoneellesi. Voit tehdä sen esimerkiksi VSCodella tai GitBashilla. Tarvitset sitä varten git-repositorion osoitteen, joka löytyy Githubin repositorion etusivulta vihreästä Code-painikkeesta. Gitbashilla saat kloonattua repositorion komennolla `git clone https://github.com/neakare/lemmikkisovellus.git`
2. Tarvitset samaan kansioon myös kurssin materiaalin 1. osassa kuvatun Pythonin virtuaaliympäristön ja flask-asennuksen. Lisäksi tarvitset sqlite-asennuksen (ks. kurssimateriaalin osa 2).
3. Tietokanta luodaan schema-tiedostolla. 
4. Kun olet tehnyt yllämainitut asennukset, voit aloittaa itse testauksen. Sovellusta käytetään virtuaaliympäristössä samalla tavalla kuin kurssimateriaalissa on kuvattu osiossa 1. Alla vielä komennot ajamista varten.


### Linuxilla
`$ cd "laita tähän sen kansion osoite johon kloonasit sovelluksen"`  
`$ python3 -m venv venv`  
`$ source venv/bin/activate`  
`$ pip install flask`  
sqliten voit kopioida samaan kansioon esimerkiksi omasta kurssiprojektistasi.  
`$ sqlite3 database.db < schema.sql`  
`$ flask run` tai `$ flask run --debug`  

### Windowsilla
`cd "laita tähän kansion osoite johon kloonasit sovelluksen"`  
`python -m venv venv`  
`venv\Scripts\activate`  
`pip install flask`  
sqliten voit kopioida samaan kansioon esimerkiksi omasta kurssiprojektistasi. 
`sqlite3 database.db < schema.sql`  
`flask run` tai `flask run --debug`  



## 17.8. tilannekatsaus
Ensimmäisen väliarvostelun jälkeen on tehty seuraavat parannukset:

### Uudet ominaisuudet
- Lisätty ulkoasu koko sivustolle (lisätty main.css ja index.html)
- Lisätty mahdollisuus lisätä, muokata ja poistaa kuvia käyttäjälle ja lemmikille
- Lisätty valmiit luokat lemmikkien aktiivisuustasolle ja ruokahalulle. Luokkien arvot ovat valmiina tietokannassa ja käyttäjä valitsee arvon pudotusvalikosta. Lisätty mahdollisuus muokata lemmikille asetettuja arvoja (käyttäjä voi muokata vain lemmikkejä, jotka on itse lisännyt).
- Lisätty mahdollisuus arvostella lemmikki, muokata ja poistaa arvosteluja sekä arvostelutilastoja lemmikin sivuille.

### Muita parannuksia
- Estetty CSFR-aukko kaikilla lomakkeilla
- Korjattu virhe sisäänkirjautumisessa
- Rivitetty pitkät kommentit, jotta teksti ei vuoda yli kommenttibokseista/hajota ulkoasua.
- Käyttäjän rivinvaihdot näkyy sivulla
- Parannettu valvontaa käyttäjän lähettämille tiedoille ja ohjeistusta käyttäjälle
- Lisätty flask-viestit ja helpotettu navigointia
- Lisätty README-tiedostoon ajo-ohjeiden komennot
- Lisätty label-kuvaukset osaan lomakkeista, loput vielä työlistalla
- Lisätty alt tekstit käyttäjän ja lemmikin kuviin


