# Noodle

Noodle on web-sovellus, jota voidaan käyttää opetuksen apuvälineenä. Noodle tarjoaa erilaisia tehtäväpohjia, joiden avulla opettajat voivat suunnitella tehtäviä opiskelijoiden ratkaistavaksi. Noodle tarkastaa vastaukset automaattisesti, mikä vähentää opettajan työtaakkaa ja tarjoaa opiskelijalle välittömän palautteen. 

## Käyttäjäroolit ja päätoiminnallisuudet

* Ylläpitäjä
  * Voi luoda uusia kurssialustoja
  * Voi antaa vastuuopettajan oikeudet toiselle käyttäjälle uutta kurssia luotaessa
  * Voi poistaa kursseja ja käyttäjiä (ei vielä toteutettu)

* Käyttäjä
  * Voi liittyä kursseille ja suorittaa niiden tehtäviä
  * Voi luoda uusia tehtäviä niiden kurssien alustoille, joissa vastuuopettajana
  * Näkee kurssille ilmoittautuneet opiskelijat ja näiden saamat tehtäväpisteet (ei vielä toteutettu)

## Sovelluksen tila 9.8. (välipalautus 2)

* Sovellukseen voi nyt luoda uusia käyttäjiä, kursseja, tehtäviä ja kysymyksiä. Käyttäjän vastaukset tallentuvat tietokantaan ja ovat käyttäjälle itselleen myöhemmin tarkasteltavissa

* Kysymysvaihtoehdot ovat tällä hetkellä hyvin rajoitetut, suunnitelmana lisätä erilaisia kysymyspohjia

* Joitain toiminnallisuuksia vielä puuttuu, kuten kurssien, tehtävien ja kysymyksien poistaminen ja opettajan kurssinäkymä

* Sovelluksen ulkoasuun ei ole vielä koskettu

## Sovellus Herokussa

Sovellusta voi kokeilla [Herokussa](http://tsoha-noodle.herokuapp.com/). Voit luoda sovellukseen omat tunnukset tai käyttää admin-käyttäjää (tunnus: 'admin', salasana: 'noodleadmin'). Sovellukseen on luotu valmiiksi pari tehtävää.
