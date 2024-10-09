--
-- PostgreSQL database dump
--

-- Dumped from database version 14.13 (Ubuntu 14.13-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.13 (Ubuntu 14.13-0ubuntu0.22.04.1)

-- Started on 2024-09-18 11:46:42 -03

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


COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;


CREATE TABLE public.action_types (
    id bigint NOT NULL,
    action_type character varying NOT NULL
);


ALTER TABLE public.action_types ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.action_types_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


CREATE TABLE public.actions (
    id bigint NOT NULL,
    action_type_id bigint NOT NULL,
    user_id bigint NOT NULL,
    token character varying NOT NULL,
    "timestamp" timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    executed_timestamp timestamp with time zone
);


ALTER TABLE public.actions ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.actions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE public.currencies (
    id bigint NOT NULL,
    name character varying NOT NULL,
    name_plural character varying NOT NULL,
    symbol character varying NOT NULL
);


ALTER TABLE public.currencies ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.currency_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


CREATE TABLE public.folders (
    id bigint NOT NULL,
    uuid uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id bigint NOT NULL,
    name character varying NOT NULL
);


ALTER TABLE public.folders ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.folders_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


CREATE TABLE public.hash_types (
    id bigint NOT NULL,
    hash_type character varying NOT NULL
);


ALTER TABLE public.hash_types ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.hash_types_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


CREATE TABLE public.plan_periods (
    id bigint NOT NULL,
    name character varying NOT NULL,
    period interval NOT NULL,
    name_plural character varying NOT NULL,
    unit_name character varying NOT NULL
);


ALTER TABLE public.plan_periods ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.plan_periods_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


CREATE TABLE public.plan_prices (
    id bigint NOT NULL,
    price numeric NOT NULL,
    currency_id bigint NOT NULL,
    period_id bigint
);


ALTER TABLE public.plan_prices ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.plan_prices_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE public.plan_resource_limits (
    id bigint NOT NULL,
    plan_id bigint NOT NULL,
    resource_id bigint NOT NULL,
    "limit" bigint,
    period_id bigint
);


ALTER TABLE public.plan_resource_limits ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.plan_resource_limits_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


CREATE TABLE public.plan_resources (
    id bigint NOT NULL,
    name character varying NOT NULL,
    name_singular character varying NOT NULL
);


ALTER TABLE public.plan_resources ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.plan_resources_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


CREATE TABLE public.plans (
    id bigint NOT NULL,
    name character varying NOT NULL,
    price_id bigint NOT NULL
);


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
    hash_type_id bigint DEFAULT 1 NOT NULL,
    hash bytea NOT NULL,
    plan_id bigint DEFAULT 1 NOT NULL,
    phone character varying NOT NULL,
    login_failure_count bigint DEFAULT 0 NOT NULL,
    verified boolean DEFAULT false NOT NULL,
    full_name character varying NOT NULL,
    login_failure_timestamp timestamp with time zone,
    phone_normalized character varying NOT NULL
);



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


CREATE VIEW public.view_plan_periods AS
 SELECT p.id,
    p.name AS plan_name,
    per.name AS period_name,
    pr.price
   FROM ((public.plans p
     JOIN public.plan_prices pr ON ((p.price_id = pr.id)))
     JOIN public.plan_periods per ON ((pr.period_id = per.id)));


CREATE VIEW public.view_resources_limits AS
 SELECT rl.id,
    p.name AS plan_name,
    p_pri_per.name AS plan_period,
    pr.name AS resource_name,
    rl."limit",
    per.name AS period_name
   FROM (((((public.plan_resource_limits rl
     JOIN public.plans p ON ((rl.plan_id = p.id)))
     JOIN public.plan_prices pri ON ((p.price_id = pri.id)))
     LEFT JOIN public.plan_periods p_pri_per ON ((pri.period_id = p_pri_per.id)))
     JOIN public.plan_resources pr ON ((rl.resource_id = pr.id)))
     LEFT JOIN public.plan_periods per ON ((rl.period_id = per.id)))
  ORDER BY p.id;


INSERT INTO public.action_types OVERRIDING SYSTEM VALUE VALUES (1, 'confirm_email');
INSERT INTO public.action_types OVERRIDING SYSTEM VALUE VALUES (2, 'confirm_password_reset');
INSERT INTO public.action_types OVERRIDING SYSTEM VALUE VALUES (3, 'confirm_email_change_original');
INSERT INTO public.action_types OVERRIDING SYSTEM VALUE VALUES (4, 'confirm_email_change_new');


INSERT INTO public.currencies OVERRIDING SYSTEM VALUE VALUES (1, 'Real', 'Reais', 'R$');
INSERT INTO public.currencies OVERRIDING SYSTEM VALUE VALUES (2, 'Dólar', 'Dólares', 'US$');


INSERT INTO public.hash_types OVERRIDING SYSTEM VALUE VALUES (1, 'bcrypt');


INSERT INTO public.plan_periods OVERRIDING SYSTEM VALUE VALUES (2, 'Anual', '1 year', 'Anuais', 'Ano');
INSERT INTO public.plan_periods OVERRIDING SYSTEM VALUE VALUES (1, 'Mensal', '1 mon', 'Mensais', 'Mês');


INSERT INTO public.plan_prices OVERRIDING SYSTEM VALUE VALUES (2, 67.90, 1, 1);
INSERT INTO public.plan_prices OVERRIDING SYSTEM VALUE VALUES (3, 390.90, 1, 1);
INSERT INTO public.plan_prices OVERRIDING SYSTEM VALUE VALUES (4, 730.90, 1, 2);
INSERT INTO public.plan_prices OVERRIDING SYSTEM VALUE VALUES (5, 3982.90, 1, 2);
INSERT INTO public.plan_prices OVERRIDING SYSTEM VALUE VALUES (1, 0.00, 1, NULL);


INSERT INTO public.plan_resource_limits OVERRIDING SYSTEM VALUE VALUES (4, 2, 1, 100, 1);
INSERT INTO public.plan_resource_limits OVERRIDING SYSTEM VALUE VALUES (10, 4, 1, 1200, 2);
INSERT INTO public.plan_resource_limits OVERRIDING SYSTEM VALUE VALUES (2, 1, 2, 1, NULL);
INSERT INTO public.plan_resource_limits OVERRIDING SYSTEM VALUE VALUES (3, 1, 3, 1, NULL);
INSERT INTO public.plan_resource_limits OVERRIDING SYSTEM VALUE VALUES (5, 2, 2, 1, NULL);
INSERT INTO public.plan_resource_limits OVERRIDING SYSTEM VALUE VALUES (8, 3, 2, 5, NULL);
INSERT INTO public.plan_resource_limits OVERRIDING SYSTEM VALUE VALUES (11, 4, 2, 1, NULL);
INSERT INTO public.plan_resource_limits OVERRIDING SYSTEM VALUE VALUES (12, 4, 3, NULL, NULL);
INSERT INTO public.plan_resource_limits OVERRIDING SYSTEM VALUE VALUES (9, 3, 3, NULL, NULL);
INSERT INTO public.plan_resource_limits OVERRIDING SYSTEM VALUE VALUES (13, 5, 1, 6000, 2);
INSERT INTO public.plan_resource_limits OVERRIDING SYSTEM VALUE VALUES (14, 5, 2, NULL, NULL);
INSERT INTO public.plan_resource_limits OVERRIDING SYSTEM VALUE VALUES (15, 5, 3, NULL, NULL);
INSERT INTO public.plan_resource_limits OVERRIDING SYSTEM VALUE VALUES (1, 1, 1, 10, NULL);
INSERT INTO public.plan_resource_limits OVERRIDING SYSTEM VALUE VALUES (6, 2, 3, NULL, NULL);
INSERT INTO public.plan_resource_limits OVERRIDING SYSTEM VALUE VALUES (7, 3, 1, 500, 1);


INSERT INTO public.plan_resources OVERRIDING SYSTEM VALUE VALUES (1, 'Usos de IA', 'Uso de IA');
INSERT INTO public.plan_resources OVERRIDING SYSTEM VALUE VALUES (2, 'Usuários', 'Usuário');
INSERT INTO public.plan_resources OVERRIDING SYSTEM VALUE VALUES (3, 'Projetos', 'Projeto');


INSERT INTO public.plans OVERRIDING SYSTEM VALUE VALUES (1, 'Gratuito', 1);
INSERT INTO public.plans OVERRIDING SYSTEM VALUE VALUES (2, 'Individual Mensal', 2);
INSERT INTO public.plans OVERRIDING SYSTEM VALUE VALUES (3, 'Empresarial Mensal', 3);
INSERT INTO public.plans OVERRIDING SYSTEM VALUE VALUES (4, 'Individual Anual', 4);
INSERT INTO public.plans OVERRIDING SYSTEM VALUE VALUES (5, 'Empresarial Anual', 5);


INSERT INTO public.versions VALUES ('202407231657', '2024-07-23 16:57:00-03');
INSERT INTO public.versions VALUES ('202408060938', '2024-08-06 09:38:00-03');
INSERT INTO public.versions VALUES ('202408120636', '2024-08-12 06:36:00-03');
INSERT INTO public.versions VALUES ('202408181542', '2024-08-18 15:42:00-03');
INSERT INTO public.versions VALUES ('202409041044', '2024-09-04 10:44:00-03');
INSERT INTO public.versions VALUES ('202409161614', '2024-09-16 16:14:00-03');
INSERT INTO public.versions VALUES ('202409191606', '2024-09-19 16:06:00-03');
INSERT INTO public.versions VALUES ('202409201513', '2024-09-20 15:13:00-03');


SELECT pg_catalog.setval('public.action_types_id_seq', 4, true);


SELECT pg_catalog.setval('public.currency_id_seq', 2, true);


SELECT pg_catalog.setval('public.hash_types_id_seq', 1, true);


SELECT pg_catalog.setval('public.plan_periods_id_seq', 2, true);


SELECT pg_catalog.setval('public.plan_prices_id_seq', 5, true);


SELECT pg_catalog.setval('public.plan_resource_limits_id_seq', 15, true);


SELECT pg_catalog.setval('public.plan_resources_id_seq', 3, true);


SELECT pg_catalog.setval('public.plans_id_seq', 5, true);


ALTER TABLE ONLY public.action_types
    ADD CONSTRAINT action_types_pk PRIMARY KEY (id);


ALTER TABLE ONLY public.actions
    ADD CONSTRAINT actions_pk PRIMARY KEY (id);


ALTER TABLE ONLY public.actions
    ADD CONSTRAINT actions_token_unique UNIQUE (token);


ALTER TABLE ONLY public.currencies
    ADD CONSTRAINT currencies_name_plural_unique UNIQUE (name_plural);


ALTER TABLE ONLY public.currencies
    ADD CONSTRAINT currencies_name_unique UNIQUE (name);


ALTER TABLE ONLY public.currencies
    ADD CONSTRAINT currencies_pk PRIMARY KEY (id);


ALTER TABLE ONLY public.currencies
    ADD CONSTRAINT currencies_symbol_unique UNIQUE (symbol);


ALTER TABLE ONLY public.folders
    ADD CONSTRAINT folders_name_user_id_unique UNIQUE (name, user_id);


ALTER TABLE ONLY public.folders
    ADD CONSTRAINT folders_pk PRIMARY KEY (id);


ALTER TABLE ONLY public.folders
    ADD CONSTRAINT folders_uuid_unique UNIQUE (uuid);


ALTER TABLE ONLY public.hash_types
    ADD CONSTRAINT hash_types_pk PRIMARY KEY (id);


ALTER TABLE ONLY public.hash_types
    ADD CONSTRAINT hash_types_unique UNIQUE (hash_type);


ALTER TABLE ONLY public.plan_periods
    ADD CONSTRAINT plan_periods_name_plural_unique UNIQUE (name_plural);


ALTER TABLE ONLY public.plan_periods
    ADD CONSTRAINT plan_periods_name_unique UNIQUE (name);


ALTER TABLE ONLY public.plan_periods
    ADD CONSTRAINT plan_periods_pk PRIMARY KEY (id);


ALTER TABLE ONLY public.plan_periods
    ADD CONSTRAINT plan_periods_unit_name_unique UNIQUE (unit_name);


ALTER TABLE ONLY public.plan_prices
    ADD CONSTRAINT plan_prices_pk PRIMARY KEY (id);


ALTER TABLE ONLY public.plan_resource_limits
    ADD CONSTRAINT plan_resource_limits_pk PRIMARY KEY (id);


ALTER TABLE ONLY public.plan_resources
    ADD CONSTRAINT plan_resources_name_singular_unique UNIQUE (name_singular);


ALTER TABLE ONLY public.plan_resources
    ADD CONSTRAINT plan_resources_name_unique UNIQUE (name);


ALTER TABLE ONLY public.plan_resources
    ADD CONSTRAINT plan_resources_pk PRIMARY KEY (id);


ALTER TABLE ONLY public.plans
    ADD CONSTRAINT plans_pk PRIMARY KEY (id);


ALTER TABLE ONLY public.plans
    ADD CONSTRAINT plans_unique UNIQUE (name);


ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_unique UNIQUE (email);


ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_name_unique UNIQUE (user_name);


ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_phone_normalized_unique UNIQUE (phone_normalized);


ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pk PRIMARY KEY (id);


ALTER TABLE ONLY public.versions
    ADD CONSTRAINT versions_pk PRIMARY KEY (version);


ALTER TABLE ONLY public.actions
    ADD CONSTRAINT actions_action_types_fk FOREIGN KEY (action_type_id) REFERENCES public.action_types(id);


ALTER TABLE ONLY public.actions
    ADD CONSTRAINT actions_users_fk FOREIGN KEY (user_id) REFERENCES public.users(id);


ALTER TABLE ONLY public.folders
    ADD CONSTRAINT folders_users_fk FOREIGN KEY (user_id) REFERENCES public.users(id);


ALTER TABLE ONLY public.plan_prices
    ADD CONSTRAINT plan_prices_currencies_fk FOREIGN KEY (currency_id) REFERENCES public.currencies(id);


ALTER TABLE ONLY public.plan_prices
    ADD CONSTRAINT plan_prices_plan_periods_fk FOREIGN KEY (period_id) REFERENCES public.plan_periods(id);


ALTER TABLE ONLY public.plan_resource_limits
    ADD CONSTRAINT plan_resource_limits_plan_periods_fk FOREIGN KEY (period_id) REFERENCES public.plan_periods(id);


ALTER TABLE ONLY public.plan_resource_limits
    ADD CONSTRAINT plan_resource_limits_plan_resources_fk FOREIGN KEY (resource_id) REFERENCES public.plan_resources(id);


ALTER TABLE ONLY public.plan_resource_limits
    ADD CONSTRAINT plan_resource_limits_plans_fk FOREIGN KEY (plan_id) REFERENCES public.plans(id);


ALTER TABLE ONLY public.plans
    ADD CONSTRAINT plans_plan_prices_fk FOREIGN KEY (price_id) REFERENCES public.plan_prices(id);


ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_hash_types_fk FOREIGN KEY (hash_type_id) REFERENCES public.hash_types(id);


ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_plans_fk FOREIGN KEY (plan_id) REFERENCES public.plans(id);


-- Completed on 2024-09-18 11:46:43 -03

--
-- PostgreSQL database dump complete
--

