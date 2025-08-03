# lemmikkisovellus

Lemmikkisovelluksella on tällä hetkellä seuraavat ominaisuudet:
1. Sovelluksessa käyttäjät pystyvät tallentamaan lemmikkien tietoja. Lemmikin tiedoissa lukee sen eläinlaji, nimi ja rotu.
2. Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen ja ulos siitä.
3. Käyttäjä näkee sovellukseen lisätyt lemmikit.
4. Käyttäjä pystyy lisäämään lemmikkejä ja muokkaamaan niiden tietoja ja poistamaan niitä.
5. Käyttäjä näkee lemmikkien tietoihin jätetyt kommentit
6. Käyttäjä pystyy kommentoimaan lemmikkejä, muokkaamaan kommenttia ja poistamaan sen.
5. Käyttäjä pystyy etsimään lemmikkejä sekä kommentteja hakusanalla.

Tässä pääasiallinen tietokohde on lemmikki ja toissijainen tietokohde on kommentti lemmikin tietoihin.

Yleistä toteutuksesta:

Sovelluksen tietokannan saat luotua schema.sql tiedoston avulla. Lisäksi sovelluksen git-kansiosta löytyy Templates-kansiosta käytetyt html-sivupohjat ja sovelluksen käyttämät py-tiedostot. petinfo.py -tiedostossa on toteutettu kaikki metodit, joissa määritellään pet ja messages -tauluihin liittyvät SQL-kyselyt. Users-talulle on oma users.py -tiedosto. 

Testausohjeet:

1. Aloita testaaminen kloonaamalla git-repositorio tietokoneellesi. Voit tehdä sen esimerkiksi VSCodella tai GitBashilla. Tarvitset sitä varten git-repositorion osoitteen, joka löytyy Githubin repositorion etusivulta vihreästä Code-painikkeesta. 

2. Tarvitset samaan kansioon myös kurssin materiaalin 1. osassa kuvatun Pythonin virtuaaliympäristön ja flask-asennuksen. Lisäksi tarvitset sqlite-asennuksen (ks. kurssimateriaalin osa 2)

3. Tietokanta luodaan schema-tiedostolla. Ohje löytyy kurssimateriaalin 4. osasta

4. Kun olet tehnyt yllämainitut asennukset, voit aloittaa itse testauksen. Sovellusta käytetään virtuaaliympäristössä samalla tavalla kuin kurssimateriaalissa on kuvattu osiossa 1.


Sovelluksen tämänhetkiset toiminnallisuudet ja niiden testaaminen
Sovellus on vielä kehitysvaiheessa ja siinä ei sen takia ole vielä ihan kaikkia ominaisuuksia ja esimerkiksi ulkoasu on kovin viimeistelemätön. Alle on listattu asioita, joita olisi hyvä testata ja joita voi jo testata:

1. Luo uusia käyttäjiä tietokantaan, kirjaudu sisään ja ulos eri käyttäjillä
2. Luo uusia lemmikkejä tietokantaan, muokkaa niiden tietoja ja poista lemmikkejä.
3. Kommentoi lemmikkien tietoja, muokkaa kommentteja ja poista niitä.
4. Hae lemmikkejä ja kommentteja haku-toiminnolla.



