use ms2_db;

-- Drop table
DROP TABLE IF EXISTS waitlist;
DROP TABLE IF EXISTS sessions;
DROP TABLE IF EXISTS users;

-- Create table
DROP TABLE IF EXISTS users;
CREATE TABLE users
(
    userid int auto_increment PRIMARY KEY,
    email varchar(255) unique NOT NULL ,
    `password` varchar(255) NOT NULL ,
    username varchar(255) default 'Badminton Player',
    sex	ENUM('Female', 'Male', 'Others'),
    birthday DATE,
    preference ENUM('Double', 'Single'),
    credits	int default 100
);

CREATE TABLE sessions
(
    sessionid int auto_increment primary key,
    begintime DATETIME not null,
    endtime DATETIME not null,
    capacity int default 8
);

CREATE TABLE waitlist
(
    sessionid int,
    userid int,
    updatetime DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    notes varchar(255),
    PRIMARY KEY (sessionid, userid),
    FOREIGN KEY (sessionid) REFERENCES sessions(sessionid) ON DELETE CASCADE,
    FOREIGN KEY (userid) REFERENCES users(userid) ON DELETE CASCADE

);


-- Insertion
INSERT INTO users (email, password, username, sex, birthday, credits ) VALUES ('test5@test.com', '123456', 'panda', 'female', '2014-01-01', '90');
INSERT INTO users (email, password, username, sex, birthday, credits ) VALUES ('test4@test.com', '123456', 'zebra', 'female', '2014-01-01', '60');
INSERT INTO users (email, password, username, sex, birthday, credits ) VALUES ('test3@test.com', '123456', 'orange', 'female', '2015-01-01', '0');
INSERT INTO users (email, password, username, sex, birthday, credits ) VALUES ('test2@test.com', '123456', 'apple', 'male', '2017-01-01', '40');
INSERT INTO users (email, password, username, sex, birthday, credits ) VALUES ('test1@test.com', '123456', 'banana', 'male', '2022-01-01', '100');
INSERT INTO users (email, password, username, sex, birthday, credits ) VALUES ('test@test.com', '123456', 'mushroom', 'male', '2021-01-01', '100');
INSERT INTO users (email, password, username, sex, birthday) VALUES ('test6@test.com', '123456', 'panda', 'female', '2010-01-01');

INSERT INTO sessions (begintime, endtime) VALUES ('2022-10-17 18:30:00', '2022-10-17 19:30:00');
INSERT INTO sessions (begintime, endtime) VALUES ('2022-10-18 18:30:00', '2022-10-18 19:30:00');
INSERT INTO sessions (begintime, endtime) VALUES ('2022-10-19 18:30:00', '2022-10-19 19:30:00');
INSERT INTO sessions (begintime, endtime) VALUES ('2022-10-20 18:30:00', '2022-10-20 19:30:00');

INSERT INTO waitlist (sessionid, userid, notes) VALUES (1,1, 'Enjoy');
INSERT INTO waitlist (sessionid, userid, notes) VALUES (1,3, 'Welcome');
INSERT INTO waitlist (sessionid, userid) VALUES (1,6);
INSERT INTO waitlist (sessionid, userid) VALUES (2,1);
INSERT INTO waitlist (sessionid, userid) VALUES (2,2);
INSERT INTO waitlist (sessionid, userid) VALUES (2,4);
INSERT INTO waitlist (sessionid, userid) VALUES (2,5);
DELETE FROM waitlist WHERE userid=1 AND sessionid=1;

SELECT * FROM users;
SELECT * FROM sessions;
SELECT * FROM waitlist;

