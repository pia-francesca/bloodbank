DROP TABLE IF EXISTS bloodbank;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS bloodstock;

CREATE TABLE bloodbank (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(25) UNIQUE NOT NULL
);

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username VARCHAR(30) UNIQUE NOT NULL,
  password VARCHAR(30) NOT NULL,
  bloodbank_id INTEGER NOT NULL,
  FOREIGN KEY (bloodbank_id) REFERENCES bloodbank (id)
);


CREATE TABLE bloodstock (
  id INTEGER(5) PRIMARY KEY,
  blood_type VARCHAR(25) NOT NULL,
  blood_group VARCHAR(2) NOT NULL,
  rhesus CHAR(1) NOT NULL,
  created TEXT NOT NULL,
  room VARCHAR(10),
  fridge VARCHAR(10),
  shelf VARCHAR(10),
  bloodbank_id INTEGER NOT NULL,
  FOREIGN KEY (bloodbank_id) REFERENCES bloodbank (id)
);
