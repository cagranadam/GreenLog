CREATE TABLE od_greenlog (
    origin INT,
    destination INT,
    distance INT,
    time INT
);
SELECT * FROM od_greenlog;

CREATE TABLE people_greenlog (
    id INT,
    E_mail Text,
    Paswoord Text,
    Straat Text,
	Hnr Int
);
ALTER TABLE people_greenlog
ALTER COLUMN hnr TYPE VARCHAR;

ALTER TABLE people_greenlog
RENAME COLUMN E_mail to email;

SELECT * FROM people_greenlog;

CREATE TABLE order_greenlog (
DeliveryorderID VARCHAR,
id VARCHAR,
available_options VARCHAR,
chosen_option VARCHAR
);

ALTER TABLE order_greenlog
RENAME COLUMN personid TO id
SELECT * FROM order_greenlog

CREATE TABLE delivery_greenlog (
email VARCHAR,
Delivery_adress VARCHAR,
DeliveryorderID VARCHAR, 
Expected_delivery VARCHAR);

SELECT * FROM delivery_greenlog

SELECT datname FROM pg_database;
SELECT * FROM pg_user;
SHOW port;

SELECT email, paswoord FROM people_greenlog WHERE email = 'viviane.callaert@telenet.be';




