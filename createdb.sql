PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE categories (
        category_id integer primary key autoincrement,
        title varchar(100),
        description text(255)
    );

CREATE TABLE IF NOT EXISTS "admins" (
admin_id integer primary key autoincrement,
tg_id bigint UNIQUE,
admin_username varchar(100) not null,
admin_first_name varchar(100),
admin_last_name varchar(100),
description text(255)
);

CREATE TABLE IF NOT EXISTS "channels"(
channel_id integer primary key autoincrement,
channel_name varchar(100) not null unique,
description text(255),
category_id integer default 1,
admin_id integer,
FOREIGN KEY(category_id) REFERENCES categories(category_id),
FOREIGN KEY(admin_id) REFERENCES admins(admin_id));

CREATE VIEW admin_and_channels as select admins.tg_id, admins.admin_username, admins.admin_first_name, admins.admin_last_name, channels.channel_name, channels.description, channels.category_id, channels.admin_id, categories.title from channels
inner join admins on channels.admin_id = admins.admin_id
inner join categories on channels.category_id == categories.category_id;
CREATE TRIGGER insert_admin_and_channels
INSTEAD OF INSERT
ON admin_and_channels
BEGIN
INSERT INTO admins (tg_id, admin_username, admin_first_name, admin_last_name)
VALUES (NEW.tg_id, NEW.admin_username, NEW.admin_first_name, NEW.admin_last_name);
INSERT INTO channels (channel_name, description, category_id, admin_id)
VALUES (NEW.channel_name, NEW.description, NEW.category_id, last_insert_rowid());
END;
CREATE INDEX idx_channel_name on channels (channel_name);
COMMIT;
