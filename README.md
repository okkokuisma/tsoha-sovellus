# Noodle

Noodle on web-sovellus, jota voidaan käyttää opetuksen apuvälineenä. Noodle tarjoaa erilaisia tehtäväpohjia, joiden avulla opettajat voivat suunnitella tehtäviä opiskelijoiden ratkaistavaksi. Noodle tarkastaa vastaukset automaattisesti, mikä vähentää opettajan työtaakkaa ja tarjoaa opiskelijalle välittömän palautteen. Vastaukset tallentuvat tietokantaan, jolloin opettaja voi tarkastella opiskelijoiden tuloksia ja kehihtystä kurssin aikana.

## Käyttäjäroolit ja päätoiminnallisuudet

* Ylläpitäjä
	* Voi luoda uusia kurssialustoja
	* Voi antaa vastuuopettajan oikeudet toiselle käyttäjälle uutta kurssia luotaessa
	* Voi poistaa kursseja ja tehtäviä

* Vastuuopettaja
	* Voi lisätä kurssilleen uusia tehtäviä ja kysymyksiä
	* Voi poistaa kurssiltaan tehtäviä ja kysymyksiä
	* Näkee kurssille ilmoittautuneet opiskelijat
	* Näkee kurssille ilmottautuineiden opiskelijoiden vastaukset ja tulokset

* Käyttäjä
	* Voi liittyä kursseille ja suorittaa niiden tehtäviä
	* Voi tarkastella jälkikäteen omia vastauksia ja tuloksia

## Sovellus Herokussa

Sovellusta voi kokeilla [Herokussa](http://tsoha-noodle.herokuapp.com/). Voit luoda sovellukseen omat tunnukset tai käyttää admin-käyttäjää (tunnus: 'admin', salasana: 'noodleadmin').
