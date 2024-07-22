CREATE TABLE IF NOT EXISTS "users" (
	"tg_user_id"	INTEGER NOT NULL UNIQUE,
	"tg_chat_id"	INTEGER NOT NULL UNIQUE,
	"region_id"	INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS "products" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	"description"	TEXT NOT NULL,
	"photo"	BLOB NOT NULL UNIQUE,
	"price"	INTEGER NOT NULL,
	"seller_tg_id"	INTEGER NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "regions" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	PRIMARY KEY("id")
);
CREATE INDEX "products_index" ON "products" (
	"name"
);
CREATE INDEX "regions_index" ON "regions" (
	"id",
	"name",
	"description"
);