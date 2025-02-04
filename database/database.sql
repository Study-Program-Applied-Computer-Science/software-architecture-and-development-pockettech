DROP SCHEMA IF EXISTS "FinancePlanner" ;

CREATE SCHEMA IF NOT EXISTS "FinancePlanner";

DROP TABLE IF EXISTS "FinancePlanner"."Country";

CREATE TABLE IF NOT EXISTS "FinancePlanner"."Country"
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 400 CACHE 1 ),
    country text COLLATE pg_catalog."default" NOT NULL,
    currency text COLLATE pg_catalog."default" NOT NULL,
    phone_code text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Country_pkey" PRIMARY KEY (id),
    CONSTRAINT "UNIQUE_COUNTRY_PHONE_CODE" UNIQUE (phone_code)
);

DROP TABLE IF EXISTS "FinancePlanner"."User";

CREATE TABLE IF NOT EXISTS "FinancePlanner"."User"
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    name text COLLATE pg_catalog."default" NOT NULL,
    country_id integer NOT NULL,
    email_id text COLLATE pg_catalog."default" NOT NULL,
    password text COLLATE pg_catalog."default" NOT NULL,
    phone_number text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "PK_USER" PRIMARY KEY (id),
    CONSTRAINT "UNIQUE_USER_EMAIL_ID" UNIQUE (email_id),
    CONSTRAINT "FK_USER_COUNTRY_COUNTRY_ID" FOREIGN KEY (country_id)
        REFERENCES "FinancePlanner"."Country" (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

DROP TABLE IF EXISTS "FinancePlanner"."TransactionsCategory";

CREATE TABLE IF NOT EXISTS "FinancePlanner"."TransactionsCategory"
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 400 CACHE 1 ),
    category text COLLATE pg_catalog."default" NOT NULL,
    expense boolean NOT NULL DEFAULT true,
    CONSTRAINT "TransactionsCategory_pkey" PRIMARY KEY (id)
);

DROP TABLE IF EXISTS "FinancePlanner"."Transaction";

CREATE TABLE IF NOT EXISTS "FinancePlanner"."Transaction"
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    "timestamp" timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    recording_user_id uuid NOT NULL,
    credit_user_id uuid,
    debit_user_id uuid,
    other_party text COLLATE pg_catalog."default",
    heading text COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default",
    transaction_mode text COLLATE pg_catalog."default" NOT NULL,
    shared_transaction boolean NOT NULL,
    category integer NOT NULL,
    amount numeric NOT NULL,
    currency_code integer NOT NULL,
    CONSTRAINT "Transaction_pkey" PRIMARY KEY (id),
    CONSTRAINT "FK_TRANSACTION_COUNTRY__CURRENCY_CODE" FOREIGN KEY (currency_code)
        REFERENCES "FinancePlanner"."Country" (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT "FK_TRANSACTION_TRANSACTION_CATEGORY__CATEGORY" FOREIGN KEY (category)
        REFERENCES "FinancePlanner"."TransactionsCategory" (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT "FK_TRANSACTION_USER__CREDIT_USER_ID" FOREIGN KEY (credit_user_id)
        REFERENCES "FinancePlanner"."User" (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT "FK_TRANSACTION_USER__DEBIT_USER_ID" FOREIGN KEY (debit_user_id)
        REFERENCES "FinancePlanner"."User" (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT "FK_TRANSACTION_USER__RECORDING_USER_ID" FOREIGN KEY (recording_user_id)
        REFERENCES "FinancePlanner"."User" (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS "FinancePlanner"."Budget";

CREATE TABLE IF NOT EXISTS "FinancePlanner"."Budget"
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    category_id uuid NOT NULL,
    amount numeric NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    currency_id integer NOT NULL,
    CONSTRAINT "Budget_pkey" PRIMARY KEY (id),
    CONSTRAINT "FK_BUDGET_COUNTRY__CURRENCY_ID" FOREIGN KEY (currency_id)
        REFERENCES "FinancePlanner"."Country" (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT "FK_BUDGET_USER_TRANSACTION_CATEGORY__CATEGORY_ID" FOREIGN KEY (category_id)
        REFERENCES "FinancePlanner"."UserTransactionsCategory" (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

INSERT INTO "FinancePlanner"."Country"(country, currency, phone_code) VALUES ('Germany', 'EUR', '+49');

INSERT INTO "FinancePlanner"."Country"(country, currency, phone_code) VALUES ('India', 'INR', '+91');

INSERT INTO "FinancePlanner"."Country"(country, currency, phone_code) VALUES ('USA', 'USD', '+1');

INSERT INTO "FinancePlanner"."TransactionsCategory"(category, expense) VALUES ('Groceries', True);

INSERT INTO "FinancePlanner"."TransactionsCategory"(category, expense) VALUES ('Clothes', True);

INSERT INTO "FinancePlanner"."TransactionsCategory"(category, expense) VALUES ('Entertainment', True);
