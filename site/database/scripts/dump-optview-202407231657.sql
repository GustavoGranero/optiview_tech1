--
-- PostgreSQL database dump
--

-- Dumped from database version 14.12 (Ubuntu 14.12-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.12 (Ubuntu 14.12-0ubuntu0.22.04.1)

-- Started on 2024-07-23 16:57:32 -03

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

--
-- TOC entry 3397 (class 1262 OID 16437)
-- Name: optview; Type: DATABASE; Schema: -; Owner: postgres
--

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

--
-- TOC entry 3 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO pg_database_owner;

--
-- TOC entry 3398 (class 0 OID 0)
-- Dependencies: 3
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 209 (class 1259 OID 16438)
-- Name: hash_types; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.hash_types (
    id bigint NOT NULL,
    hash_type character varying NOT NULL
);


ALTER TABLE public.hash_types OWNER TO postgres;

--
-- TOC entry 210 (class 1259 OID 16443)
-- Name: hash_types_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.hash_types ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.hash_types_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 211 (class 1259 OID 16444)
-- Name: plans; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.plans (
    id bigint NOT NULL,
    name character varying NOT NULL
);


ALTER TABLE public.plans OWNER TO postgres;

--
-- TOC entry 212 (class 1259 OID 16449)
-- Name: plans_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.plans ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.plans_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 213 (class 1259 OID 16450)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

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

--
-- TOC entry 214 (class 1259 OID 16457)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.users ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 215 (class 1259 OID 16458)
-- Name: versions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.versions (
    version character varying NOT NULL,
    "timestamp" timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.versions OWNER TO postgres;

--
-- TOC entry 3385 (class 0 OID 16438)
-- Dependencies: 209
-- Data for Name: hash_types; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.hash_types OVERRIDING SYSTEM VALUE VALUES (1, 'bcrypt');


--
-- TOC entry 3387 (class 0 OID 16444)
-- Dependencies: 211
-- Data for Name: plans; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.plans OVERRIDING SYSTEM VALUE VALUES (1, 'Gratuito');
INSERT INTO public.plans OVERRIDING SYSTEM VALUE VALUES (2, 'Individual');
INSERT INTO public.plans OVERRIDING SYSTEM VALUE VALUES (3, 'Empresarial');


--
-- TOC entry 3391 (class 0 OID 16458)
-- Dependencies: 215
-- Data for Name: versions; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.versions VALUES ('202407190916', '2024-07-17 18:42:56.516012-03');


--
-- TOC entry 3399 (class 0 OID 0)
-- Dependencies: 210
-- Name: hash_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.hash_types_id_seq', 1, true);


--
-- TOC entry 3400 (class 0 OID 0)
-- Dependencies: 212
-- Name: plans_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.plans_id_seq', 3, true);


--
-- TOC entry 3401 (class 0 OID 0)
-- Dependencies: 214
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 7, true);


--
-- TOC entry 3229 (class 2606 OID 16465)
-- Name: hash_types hash_types_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hash_types
    ADD CONSTRAINT hash_types_pk PRIMARY KEY (id);


--
-- TOC entry 3231 (class 2606 OID 16467)
-- Name: hash_types hash_types_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hash_types
    ADD CONSTRAINT hash_types_unique UNIQUE (hash_type);


--
-- TOC entry 3233 (class 2606 OID 16469)
-- Name: plans plans_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plans
    ADD CONSTRAINT plans_pk PRIMARY KEY (id);


--
-- TOC entry 3235 (class 2606 OID 16471)
-- Name: plans plans_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plans
    ADD CONSTRAINT plans_unique UNIQUE (name);


--
-- TOC entry 3237 (class 2606 OID 16473)
-- Name: users users_email_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_unique UNIQUE (email);


--
-- TOC entry 3239 (class 2606 OID 16475)
-- Name: users users_name_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_name_unique UNIQUE (user_name);


--
-- TOC entry 3241 (class 2606 OID 16477)
-- Name: users users_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pk PRIMARY KEY (id);


--
-- TOC entry 3243 (class 2606 OID 16479)
-- Name: versions versions_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.versions
    ADD CONSTRAINT versions_pk PRIMARY KEY (version);


--
-- TOC entry 3245 (class 2606 OID 16492)
-- Name: users users_hash_types_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_hash_types_fk FOREIGN KEY (hash_type) REFERENCES public.hash_types(id);


--
-- TOC entry 3244 (class 2606 OID 16485)
-- Name: users users_plans_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_plans_fk FOREIGN KEY (plan_id) REFERENCES public.plans(id);


-- Completed on 2024-07-23 16:57:33 -03

--
-- PostgreSQL database dump complete
--

