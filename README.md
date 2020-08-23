# Noodle

Noodle on web-sovellus, jota voidaan käyttää opetuksen apuvälineenä. Noodle tarjoaa erilaisia tehtäväpohjia, joiden avulla opettajat voivat suunnitella tehtäviä opiskelijoiden ratkaistavaksi. Noodle tarkastaa vastaukset automaattisesti, mikä vähentää opettajan työtaakkaa ja tarjoaa opiskelijalle välittömän palautteen. 

## Käyttäjäroolit ja päätoiminnallisuudet

* Ylläpitäjä
	* Voi luoda uusia kurssialustoja
	* Voi antaa vastuuopettajan oikeudet toiselle käyttäjälle uutta kurssia luotaessa
	* Voi poistaa kursseja ja tehtäviä (ei vielä toteutettu)

* Vastuuopettaja
	* Voi lisätä kurssille uusia tehtäviä ja kysymyksiä
	* Näkee kurssille ilmoittautuneet opiskelijat ja näiden saamat tulokset tehtävistä

* Käyttäjä
	* Voi liittyä kursseille ja suorittaa niiden tehtäviä

## Sovelluksen tila 9.8. (välipalautus 2)

* Sovellukseen voi nyt luoda uusia käyttäjiä, kursseja, tehtäviä ja kysymyksiä. Käyttäjän vastaukset tallentuvat tietokantaan ja ovat käyttäjälle itselleen myöhemmin tarkasteltavissa

* Kysymysvaihtoehdot ovat tällä hetkellä hyvin rajoitetut, suunnitelmana lisätä erilaisia kysymyspohjia

* Joitain toiminnallisuuksia vielä puuttuu, kuten kurssien, tehtävien ja kysymyksien poistaminen ja opettajan kurssinäkymä

* Sovelluksen ulkoasuun ei ole vielä koskettu

## Sovelluksen tila 23.8. (välipalautus 3)

* Opettajan kurssinäkymä lisätty: vastuuopettaja voi nyt lisätä ja poistaa kysymyksiä myös tehtävän lisäämisen jälkeen ja tarkastella kurssille ilmoittautuneiden opiskelijoiden tuloksia.

* Kursseille täytyy nyt ilmoittautua ennen kuin kurssin tehtäviä voi suorittaa. Ilmoittautumisia varten tietokantaan on luotu uusi taulu.

* Kurssin voi nyt suojata halutessaan kurssiavaimella.

* Pienempiä uusia toiminnallisuuksia:
	* hakutoiminto kursseille/mahdollisuus nähdä vain kurssit, joille ilmoittautunut
	* admin voi nyt lisätä käyttäjille opettajastatuksen ja kurssien vastuuopettajaksi voi valita vain käyttäjän, jolla on tämä status

* Vielä kehitettävää:
	* tietoturvassa aukkoja (CSRF-haavoittuvuus)
	* kysymyspohjia edelleen vain kaksi erilaista
	* sovelluksen ulkoasu vielä raaka
	* ajatuksena lisätä vastuuopettajille mahdollisuus nähdä opiskelijoiden vastaukset pelkkien pistemäärien lisäksi
	* vastuupettajalle mahdollisuus poistaa tehtäviä ja adminille mahdollisuus poistaa kursseja

## Sovellus Herokussa

Sovellusta voi kokeilla [Herokussa](http://tsoha-noodle.herokuapp.com/). Voit luoda sovellukseen omat tunnukset tai käyttää admin-käyttäjää (tunnus: 'admin', salasana: 'noodleadmin').
