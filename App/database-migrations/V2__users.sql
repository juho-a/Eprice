DROP TABLE IF EXISTS users;
CREATE TYPE user_role AS ENUM ('user', 'admin');


CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email TEXT NOT NULL,
  password_hash TEXT NOT NULL,
  role user_role NOT NULL DEFAULT 'user'
);

CREATE UNIQUE INDEX ON users(lower(email));