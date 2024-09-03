SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;



CREATE DATABASE optview WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'pt_BR.UTF-8';


ALTER DATABASE optview OWNER TO postgres;

\connect optview

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;


CREATE SCHEMA public;

ALTER SCHEMA public OWNER TO pg_database_owner;

COMMENT ON SCHEMA public IS 'standard public schema';

SET default_tablespace = '';

SET default_table_access_method = heap;


CREATE TABLE public.hash_types (
    id bigint NOT NULL,
    hash_type character varying NOT NULL
);

ALTER TABLE public.hash_types OWNER TO postgres;

ALTER TABLE public.hash_types ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.hash_types_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE public.plans (
    id bigint NOT NULL,
    name character varying NOT NULL
);

ALTER TABLE public.plans OWNER TO postgres;

ALTER TABLE public.plans ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.plans_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE public.users (
    id bigint NOT NULL,
    user_name character varying NOT NULL,
    email character varying NOT NULL,
    hash_type bigint DEFAULT 1 NOT NULL,
    hash bytea NOT NULL,
    plan_id bigint DEFAULT 1 NOT NULL,
    phone character varying NOT NULL,
    login_failure_count bigint DEFAULT 0 NOT NULL,
    verified boolean DEFAULT false NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

ALTER TABLE public.users ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE public.versions (
    version character varying NOT NULL,
    "timestamp" timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);

ALTER TABLE public.versions OWNER TO postgres;


INSERT INTO public.hash_types OVERRIDING SYSTEM VALUE VALUES (1, 'bcrypt');

INSERT INTO public.plans OVERRIDING SYSTEM VALUE VALUES (1, 'Gratuito');
INSERT INTO public.plans OVERRIDING SYSTEM VALUE VALUES (2, 'Individual');
INSERT INTO public.plans OVERRIDING SYSTEM VALUE VALUES (3, 'Empresarial');

SELECT pg_catalog.setval('public.hash_types_id_seq', 1, true);

SELECT pg_catalog.setval('public.plans_id_seq', 3, true);

SELECT pg_catalog.setval('public.users_id_seq', 7, true);


ALTER TABLE ONLY public.hash_types
    ADD CONSTRAINT hash_types_pk PRIMARY KEY (id);

ALTER TABLE ONLY public.hash_types
    ADD CONSTRAINT hash_types_unique UNIQUE (hash_type);

ALTER TABLE ONLY public.plans
    ADD CONSTRAINT plans_pk PRIMARY KEY (id);

ALTER TABLE ONLY public.plans
    ADD CONSTRAINT plans_unique UNIQUE (name);

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_unique UNIQUE (email);

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_name_unique UNIQUE (user_name);

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pk PRIMARY KEY (id);

ALTER TABLE ONLY public.versions
    ADD CONSTRAINT versions_pk PRIMARY KEY (version);

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_hash_types_fk FOREIGN KEY (hash_type) REFERENCES public.hash_types(id);

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_plans_fk FOREIGN KEY (plan_id) REFERENCES public.plans(id);

INSERT INTO public.versions VALUES ('202407231657', '2024-07-23 16:57:00.000000-03');