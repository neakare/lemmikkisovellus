# lemmikkisovellus

Sovelluksen tavoiteominaisuudet (ensimmäinen välipalautus):
1. Sovelluksessa käyttäjät pystyvät tallentamaan lemmikkien tietoja. Lemmikin tiedoissa lukee sen eläinlaji, nimi ja rotu.
2. Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
3. Käyttäjä pystyy lisäämään lemmikkejä ja muokkaamaan niiden tietoja ja poistamaan niitä.
4. Käyttäjä näkee sovellukseen lisätyt lemmikit.
5. Käyttäjä pystyy etsimään lemmikkejä hakusanalla.
6. Käyttäjäsivu näyttää, monenko lemmikin tiedot käyttäjä on lisännyt ja listan käyttäjän lisäämistä lemmikeistä.
7. Käyttäjä pystyy valitsemaan lemmikille yhden tai useamman luokittelun (esim. kiltti, rauhallinen, ahmatti).
8. Käyttäjä pystyy antamaan lemmikille kommentin ja arvosanan. Lemmikistä näytetään kommentit ja keskimääräinen arvosana.

Tässä pääasiallinen tietokohde on lemmikki ja toissijainen tietokohde on kommentti lemmikin tietoihin.


Testausohjeet:
Sovelluksen tietokannan saat luotua schema.sql tiedoston avulla. Lisäksi sovelluksen git-kansiosta löytyy Templates-kansiosta käytetyt html-sivupohjat ja sovelluksen käyttämät py-tiedostot. 

1. Aloita testaaminen kloonaamalla git-repositorio tietokoneellesi. Voit tehdä sen esimerkiksi VSCodella tai GitBashilla. Tarvitset sitä varten git-repositorion osoitteen, joka löytyy Githubin repositorion etusivulta vihreästä Code-painikkeesta. 

2. Tarvitset samaan kansioon myös kurssin materiaalin 1. osassa kuvatun Pythonin virtuaaliympäristön ja flask-asennuksen. Lisäksi tarvitset sqlite-asennuksen (ks. kurssimateriaalin osa 2)

3. Tietokanta luodaan schema-tiedostolla. Ohje löytyy kurssimateriaalin 4. osasta

4. Kun olet tehnyt yllämainitut asennukset, voit aloittaa itse testauksen. Sovellusta käytetään virtuaaliympäristössä samalla tavalla kuin kurssimateriaalissa on kuvattu.


Sovelluksen tämänhetkiset toiminnallisuudet ja niiden testaaminen
Yllä mainitut kohdat 1-8 kuvaavat sovelluksen tavoitetilaa. Sovellus on vielä kehitysvaiheessa ja siinä ei sen takia ole vielä ihan kaikkia ominaisuuksia. Alle on listattu asioita, joita olisi hyvä testata ja joita voi jo testata:

1. Luo uusia käyttäjiä tietokantaan, kirjaudu sisään ja ulos eri käyttäjillä
2. Luo uusia lemmikkejä tietokantaan.
3. Kommentoi lemmikkien tietoja.
4. Hae lemmikkien tietoihin jätetyistä kommenteista.



