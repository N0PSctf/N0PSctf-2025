CREATE DATABASE main_db;

USE main_db;

CREATE TABLE main_db.users (
  `id` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `public_id` VARCHAR(40),
  `username` VARCHAR(255),
  `mail` VARCHAR(60),
  `password` VARCHAR(255),
  `inscription_date` VARCHAR(255),
  `last_login_date` VARCHAR(255),
  `is_verified` BOOLEAN,
  `is_admin` BOOLEAN
);

CREATE TABLE main_db.posts (
  `id` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `post_id` VARCHAR(40),
  `title` VARCHAR(255),
  `content` TEXT,
  `creation_date` VARCHAR(255),
  `is_private` BOOLEAN,
  `user_id` INTEGER NOT NULL
);


INSERT INTO `users` (public_id, username, password, mail, inscription_date, last_login_date, is_verified, is_admin)
VALUES ('cfea660f-1d93-475c-9272-20aaba055e98', 'admin', 'scrypt:32768:8:1$kfajQDEDLSj9NoqM$e3f86e9a15b7607ce106efccb17b6a01060c0d17f4b6c54dac9ccd8d440c45dcc0c2591fadd66ef5ad56832f73da15f8166ccdd60e18fe31cd0147700ae19e51', 'admin@admin.com', '2024-07-26 13:43:45', '2024-07-28 15:12:05', 1, 1);

INSERT INTO `posts` (post_id, title, content, creation_date, is_private, user_id)
VALUES ('64d8b712-a86d-4f44-97bc-43961eb514ad', 'Welcome to this blog!', 'Please enjoy writing your public and private blogs here :) - admin', '2024-07-28 15:14:18', 0, 1);

INSERT INTO `users` (public_id, username, password, mail, inscription_date, last_login_date, is_verified, is_admin)
VALUES ('7a0dfc65-5890-4b54-a79b-c05dfce52c7d', 'noopsy123', 'scrypt:32768:8:1$XKMU7kqoUj2KNgdC$893079995786d6d822c8b706489ea2e567e66f565439b1bfa4127104ca7d7c8406a5f0ddd8d2cb95f1f8b2a3e1cd8fb2c15a53df0c4baaf05a6f96b4a222adaa', 'info@nops.re', '2024-07-28 14:02:48', '2024-08-28 02:13:58', 1, 0);

INSERT INTO `posts` (post_id, title, content, creation_date, is_private, user_id)
VALUES ('fe1982b9-368b-4d60-8a33-ed503224bb78', 'Hi from n00psy', 'Hey! I am n00psy :) I like joy, laugh and cookies!', '2024-07-28 15:14:18', 0, 2);

INSERT INTO `posts` (post_id, title, content, creation_date, is_private, user_id)
VALUES ('64d8b712-a86d-4f44-97bc-43961eb514ad', 'You have been pwned >:)', 'Nyehehe... Who would have thought N0PStopia would have been so easy to pwn? You cannot face the hacking skills of WebTopia, mwahahahahaha!!!', '2024-07-30 15:14:18', 0, 1);

INSERT INTO `posts` (post_id, title, content, creation_date, is_private, user_id)
VALUES ('0bb51c4d-8a30-4856-bfb0-a876418b9779', 'Flag (private!!!)', 'N0PS{d0t_G17_1n_Pr0DuC710n?!!}', '2024-07-28 15:13:03', 1, 2);