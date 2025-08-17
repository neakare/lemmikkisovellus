# lemmikkisovellus

## Lemmikkisovelluksella on tällä hetkellä seuraavat ominaisuudet:
1. Käyttäjä pystyyy tallentamaan lemmikkien tietoja. Lemmikin tiedoissa lukee sen eläinlaji, nimi ja rotu. 
2. Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen ja ulos siitä.
3. Käyttäjä näkee sovellukseen lisätyt lemmikit.
4. Käyttäjä pystyy lisäämään lemmikkejä ja muokkaamaan niiden tietoja ja poistamaan niitä (muokkaus ja poistaminen on mahdollista vain käyttäjän lisäämille lemmikeille).
5. Käyttäjä näkee lemmikkien tietoihin jätetyt kommentit
6. Käyttäjä pystyy kommentoimaan lemmikkejä, muokkaamaan kommenttia ja poistamaan niitä (muokkaus ja poistaminen on mahdollista vain käyttäjän lisäämille kommenteille).
7. Käyttäjä pystyy etsimään kommentteja hakusanalla. Haku hakee tällä hetkellä vain lemmikkien kommenteista.
8. käyttäjän sivuilta näkee kootusti käyttäjän lisäämät lemmikit ja kommentit.
9. Käyttäjä pystyy lisäämään kuvan itselleen käyttäjätietoihin, vaihtamaan sen ja poistamaan kuvan.
10. Käyttäjä pystyy lisäämään kuvan lisäämilleen lemmikeille, vaihtamaan ja poistamaan kuvan.

Tässä pääasiallinen tietokohde on lemmikki ja toissijainen tietokohde on kommentti lemmikin tietoihin.

## Yleistä toteutuksesta:

Sovelluksen tietokannan saat luotua schema.sql tiedoston avulla. Lisäksi sovelluksen git-kansiosta löytyy Templates-kansiosta käytetyt html-sivupohjat ja sovelluksen käyttämät py-tiedostot. petinfo.py -tiedostossa on toteutettu kaikki metodit, joissa määritellään pet ja messages -tauluihin liittyvät SQL-kyselyt. Users-tauluun liittyville sql-kyselyille on oma users.py -tiedosto. 

## Testausohjeet:

1. Aloita testaaminen kloonaamalla git-repositorio tietokoneellesi. Voit tehdä sen esimerkiksi VSCodella tai GitBashilla. Tarvitset sitä varten git-repositorion osoitteen, joka löytyy Githubin repositorion etusivulta vihreästä Code-painikkeesta. Gitbashilla saat kloonattua repositorion komennolla `git clone https://github.com/neakare/lemmikkisovellus.git`
2. Tarvitset samaan kansioon myös kurssin materiaalin 1. osassa kuvatun Pythonin virtuaaliympäristön ja flask-asennuksen. Lisäksi tarvitset sqlite-asennuksen (ks. kurssimateriaalin osa 2).
3. Tietokanta luodaan schema-tiedostolla. 
4. Kun olet tehnyt yllämainitut asennukset, voit aloittaa itse testauksen. Sovellusta käytetään virtuaaliympäristössä samalla tavalla kuin kurssimateriaalissa on kuvattu osiossa 1. Alla vielä komennot ajamista varten.


### Linuxilla
`$ cd "laita tähän kansion osoite johon kloonasit sovelluksen"`  
`$ python3 -m venv venv`  
`$ source venv/bin/activate`  
`$ pip install flask`  
sqliten voit esimerkiksi kopioida samaan kansioon omasta projektistasi.  
`$ sqlite3 database.db < schema.sql`  
`$ flask run` tai `$ flask run --debug`  

### Windowsilla
`cd "laita tähän kansion osoite johon kloonasit sovelluksen"`  
`python -m venv venv`  
`venv\Scripts\activate`  
`pip install flask`  
sqliten voit esimerkiksi kopioida samaan kansioon omasta projektistasi.  
`sqlite3 database.db < schema.sql`  
`flask run` tai `flask run --debug`  



## 17.8. toinen väliarvostelu
Ensimmäisen väliarvostelun jälkeen on tehty seuraavat parannukset:
- Estetty CSFR-aukko
- Rivitetty pitkät kommentit
- Käyttäjän rivinvaihdot näkyy sivulla
- Lisätty ulkoasu koko sivustolle
- Lisätty mahdollisuus lisätä, muokata ja poistaa kuvia käyttäjälle ja lemmikille
- Parannettu valvontaa käyttäjän lähettämille tiedoille ja ohjeistusta käyttäjälle
- Lisätty flask-viestit


