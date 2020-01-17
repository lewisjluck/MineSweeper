CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  username TEXT NOT NULL,
  email TEXT NOT NULL,
  profile_pic TEXT,
  hash TEXT,
  google_id TEXT
);
