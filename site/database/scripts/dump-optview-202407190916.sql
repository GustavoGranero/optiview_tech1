--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3
-- Dumped by pg_dump version 16.3

-- Started on 2024-07-19 09:16:47

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
-- TOC entry 4861 (class 1262 OID 16398)
-- Name: optview; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE optview WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Portuguese_Brazil.1252';


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
-- TOC entry 5 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO pg_database_owner;

--
-- TOC entry 4862 (class 0 OID 0)
-- Dependencies: 5
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 222 (class 1259 OID 16503)
-- Name: hash_types; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.hash_types (
    id bigint NOT NULL,
    hash_type character varying NOT NULL
);


ALTER TABLE public.hash_types OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16502)
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
-- TOC entry 219 (class 1259 OID 16462)
-- Name: plans; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.plans (
    id bigint NOT NULL,
    name character varying NOT NULL
);


ALTER TABLE public.plans OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 16461)
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
-- TOC entry 217 (class 1259 OID 16400)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id bigint NOT NULL,
    user_name character varying NOT NULL,
    email character varying NOT NULL,
    hash_type bigint DEFAULT 1 NOT NULL,
    hash bytea NOT NULL,
    plan_id bigint NOT NULL,
    phone character varying NOT NULL,
    login_failure_count bigint DEFAULT 0 NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 16399)
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
-- TOC entry 220 (class 1259 OID 16481)
-- Name: versions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.versions (
    version character varying NOT NULL,
    "timestamp" timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.versions OWNER TO postgres;

--
-- TOC entry 4855 (class 0 OID 16503)
-- Dependencies: 222
-- Data for Name: hash_types; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.hash_types OVERRIDING SYSTEM VALUE VALUES (1, 'bcrypt');


--
-- TOC entry 4852 (class 0 OID 16462)
-- Dependencies: 219
-- Data for Name: plans; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.plans OVERRIDING SYSTEM VALUE VALUES (1, 'Gratuito');
INSERT INTO public.plans OVERRIDING SYSTEM VALUE VALUES (2, 'Individual');
INSERT INTO public.plans OVERRIDING SYSTEM VALUE VALUES (3, 'Empresarial');


--
-- TOC entry 4853 (class 0 OID 16481)
-- Dependencies: 220
-- Data for Name: versions; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.versions VALUES ('202407190916', '2024-07-17 18:42:56.516012-03');


--
-- TOC entry 4863 (class 0 OID 0)
-- Dependencies: 221
-- Name: hash_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.hash_types_id_seq', 1, true);


--
-- TOC entry 4864 (class 0 OID 0)
-- Dependencies: 218
-- Name: plans_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.plans_id_seq', 3, true);


--
-- TOC entry 4865 (class 0 OID 0)
-- Dependencies: 216
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 1, true);


--
-- TOC entry 4701 (class 2606 OID 16509)
-- Name: hash_types hash_types_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hash_types
    ADD CONSTRAINT hash_types_pk PRIMARY KEY (id);


--
-- TOC entry 4703 (class 2606 OID 16511)
-- Name: hash_types hash_types_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hash_types
    ADD CONSTRAINT hash_types_unique UNIQUE (hash_type);


--
-- TOC entry 4695 (class 2606 OID 16466)
-- Name: plans plans_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plans
    ADD CONSTRAINT plans_pk PRIMARY KEY (id);


--
-- TOC entry 4697 (class 2606 OID 16470)
-- Name: plans plans_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plans
    ADD CONSTRAINT plans_unique UNIQUE (name);


--
-- TOC entry 4689 (class 2606 OID 16410)
-- Name: users users_email_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_unique UNIQUE (email);


--
-- TOC entry 4691 (class 2606 OID 16408)
-- Name: users users_name_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_name_unique UNIQUE (user_name);


--
-- TOC entry 4693 (class 2606 OID 16406)
-- Name: users users_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pk PRIMARY KEY (id);


--
-- TOC entry 4699 (class 2606 OID 16487)
-- Name: versions versions_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.versions
    ADD CONSTRAINT versions_pk PRIMARY KEY (version);


--
-- TOC entry 4704 (class 2606 OID 16512)
-- Name: users users_hash_types_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_hash_types_fk FOREIGN KEY (id) REFERENCES public.hash_types(id);


--
-- TOC entry 4705 (class 2606 OID 16476)
-- Name: users users_plans_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_plans_fk FOREIGN KEY (plan_id) REFERENCES public.plans(id);


-- Completed on 2024-07-19 09:16:47

--
-- PostgreSQL database dump complete
--

