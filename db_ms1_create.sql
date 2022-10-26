use ms2_db;

DROP TABLE IF EXISTS partners;
DROP TABLE IF EXISTS chatting_form;

CREATE TABLE partners
(
    Userid_from int unique PRIMARY KEY,
    Userid_to int unique NOT NULL
);

CREATE TABLE chatting_form
(
    Chat_ID int auto_increment PRIMARY KEY,
    userid_from int  NOT NULL ,
    userid_to int  NOT NULL ,
    Content longtext NOT NULL,
    Time datetime NOT NULL
);

-- Insertion
INSERT INTO partners (userid_from, userid_to) VALUES(1,2);
INSERT INTO partners (userid_from, userid_to) VALUES(3,4);
INSERT INTO partners (userid_from, userid_to) VALUES(5,6);

INSERT INTO chatting_form(Chat_ID, userid_from, userid_to, Content, Time)
VALUES(1,1,2,"Hello, how are you doing?",'2022-10-16 21:35:14');
INSERT INTO chatting_form(Chat_ID, userid_from, userid_to, Content, Time)
VALUES(2,2,1,"There is too much confsion",'2022-10-16 22:35:14');
INSERT INTO chatting_form(Chat_ID, userid_from, userid_to, Content, Time)
VALUES(3,3,2,"I cannot get relief",'2022-10-18 21:35:14');
INSERT INTO chatting_form(Chat_ID, userid_from, userid_to, Content, Time)
VALUES(4,2,6,"There is too much confsion",'2022-10-19 22:35:14');