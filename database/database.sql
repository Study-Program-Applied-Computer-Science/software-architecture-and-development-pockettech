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

DROP TABLE IF EXISTS "FinancePlanner"."UserTransactionsCategory";

CREATE TABLE IF NOT EXISTS "FinancePlanner"."UserTransactionsCategory"
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL,
    category text COLLATE pg_catalog."default" NOT NULL,
    expense boolean NOT NULL DEFAULT true,
    CONSTRAINT "UserTransactionsCategory_pkey" PRIMARY KEY (id),
    CONSTRAINT "FK_USER_TRANSACTIONS_CATEGORY_USER__USER_ID" FOREIGN KEY (user_id)
        REFERENCES "FinancePlanner"."User" (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
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
    category uuid NOT NULL,
    amount numeric NOT NULL,
    currency_code integer NOT NULL,
    CONSTRAINT "Transaction_pkey" PRIMARY KEY (id),
    CONSTRAINT "FK_TRANSACTION_COUNTRY__CURRENCY_CODE" FOREIGN KEY (currency_code)
        REFERENCES "FinancePlanner"."Country" (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT "FK_TRANSACTION_USER_TRANSACTION_CATEGORY__CATEGORY" FOREIGN KEY (category)
        REFERENCES "FinancePlanner"."UserTransactionsCategory" (id) MATCH SIMPLE
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


CREATE TABLE IF NOT EXISTS "FinancePlanner"."SharedGroup" (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    admin_user_id uuid NOT NULL,
    group_name text NOT NULL,
    CONSTRAINT "SharedGroup_pkey" PRIMARY KEY (id),
    CONSTRAINT "FK_SharedGroup_User_Admin" FOREIGN KEY (admin_user_id)
        REFERENCES "FinancePlanner"."User" (id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "FinancePlanner"."SharedGroupParticipants" (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    group_id uuid NOT NULL,
    participant_user_id uuid NOT NULL,
    CONSTRAINT "SharedGroupParticipants_pkey" PRIMARY KEY (id),
    CONSTRAINT "FK_GroupParticipants_SharedGroup_GroupID" FOREIGN KEY (group_id)
        REFERENCES "FinancePlanner"."SharedGroup" (id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT "FK_GroupParticipants_User_Participant" FOREIGN KEY (participant_user_id)
        REFERENCES "FinancePlanner"."User" (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "FinancePlanner"."ShareType" (
    id serial NOT NULL,
    share_type text NOT NULL,
    CONSTRAINT "ShareType_pkey" PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS "FinancePlanner"."PaymentStatus" (
    id serial NOT NULL,
    status text NOT NULL,
    CONSTRAINT "PaymentStatus_pkey" PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS "FinancePlanner"."SharedTransaction" (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    transaction_id uuid NOT NULL,
    group_user_id_main uuid NOT NULL,
    group_user_id_sub uuid NOT NULL,
    share_type_id integer NOT NULL,
    share_value numeric NOT NULL,
    payment_status integer NOT NULL,
    CONSTRAINT "SharedTransaction_pkey" PRIMARY KEY (id),
    CONSTRAINT "FK_SharedTransaction_Transaction_ID" FOREIGN KEY (transaction_id)
        REFERENCES "FinancePlanner"."Transaction" (id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT "FK_SharedTransaction_GroupUser_Main" FOREIGN KEY (group_user_id_main)
        REFERENCES "FinancePlanner"."SharedGroupParticipants" (id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT "FK_SharedTransaction_GroupUser_Sub" FOREIGN KEY (group_user_id_sub)
        REFERENCES "FinancePlanner"."SharedGroupParticipants" (id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT "FK_SharedTransaction_ShareType" FOREIGN KEY (share_type_id)
        REFERENCES "FinancePlanner"."ShareType" (id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT "FK_SharedTransaction_PaymentStatus" FOREIGN KEY (payment_status)
        REFERENCES "FinancePlanner"."PaymentStatus" (id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Extend FinancePlanner Schema
CREATE TABLE IF NOT EXISTS "FinancePlanner"."SharedGroup" (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    admin_user_id uuid NOT NULL,
    group_name text NOT NULL,
    CONSTRAINT "SharedGroup_pkey" PRIMARY KEY (id),
    CONSTRAINT "FK_SharedGroup_User_Admin" FOREIGN KEY (admin_user_id)
        REFERENCES "FinancePlanner"."User" (id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "FinancePlanner"."SharedGroupParticipants" (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    group_id uuid NOT NULL,
    participant_user_id uuid NOT NULL,
    CONSTRAINT "SharedGroupParticipants_pkey" PRIMARY KEY (id),
    CONSTRAINT "FK_GroupParticipants_SharedGroup_GroupID" FOREIGN KEY (group_id)
        REFERENCES "FinancePlanner"."SharedGroup" (id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT "FK_GroupParticipants_User_Participant" FOREIGN KEY (participant_user_id)
        REFERENCES "FinancePlanner"."User" (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "FinancePlanner"."ShareType" (
    id serial NOT NULL,
    share_type text NOT NULL,
    CONSTRAINT "ShareType_pkey" PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS "FinancePlanner"."PaymentStatus" (
    id serial NOT NULL,
    status text NOT NULL,
    CONSTRAINT "PaymentStatus_pkey" PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS "FinancePlanner"."SharedTransaction" (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    transaction_id uuid NOT NULL,
    group_user_id_main uuid NOT NULL,
    group_user_id_sub uuid NOT NULL,
    share_type_id integer NOT NULL,
    share_value numeric NOT NULL,
    payment_status integer NOT NULL,
    CONSTRAINT "SharedTransaction_pkey" PRIMARY KEY (id),
    CONSTRAINT "FK_SharedTransaction_Transaction_ID" FOREIGN KEY (transaction_id)
        REFERENCES "FinancePlanner"."Transaction" (id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT "FK_SharedTransaction_GroupUser_Main" FOREIGN KEY (group_user_id_main)
        REFERENCES "FinancePlanner"."SharedGroupParticipants" (id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT "FK_SharedTransaction_GroupUser_Sub" FOREIGN KEY (group_user_id_sub)
        REFERENCES "FinancePlanner"."SharedGroupParticipants" (id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT "FK_SharedTransaction_ShareType" FOREIGN KEY (share_type_id)
        REFERENCES "FinancePlanner"."ShareType" (id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT "FK_SharedTransaction_PaymentStatus" FOREIGN KEY (payment_status)
        REFERENCES "FinancePlanner"."PaymentStatus" (id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);


