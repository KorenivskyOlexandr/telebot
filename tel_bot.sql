--
-- PostgreSQL database dump
--

-- Dumped from database version 10.12 (Ubuntu 10.12-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.12 (Ubuntu 10.12-0ubuntu0.18.04.1)

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
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: knights; Type: TABLE; Schema: public; Owner: telebot
--

CREATE TABLE public.knights (
    id integer NOT NULL,
    person_id integer NOT NULL,
    title_id integer NOT NULL
);


ALTER TABLE public.knights OWNER TO telebot;

--
-- Name: knights_id_seq; Type: SEQUENCE; Schema: public; Owner: telebot
--

CREATE SEQUENCE public.knights_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.knights_id_seq OWNER TO telebot;

--
-- Name: knights_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: telebot
--

ALTER SEQUENCE public.knights_id_seq OWNED BY public.knights.id;


--
-- Name: persons; Type: TABLE; Schema: public; Owner: telebot
--

CREATE TABLE public.persons (
    id integer NOT NULL,
    person character varying NOT NULL,
    rank_id integer,
    user_id integer,
    user_name_to_call character varying
);


ALTER TABLE public.persons OWNER TO telebot;

--
-- Name: persons_call_id_seq; Type: SEQUENCE; Schema: public; Owner: telebot
--

CREATE SEQUENCE public.persons_call_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.persons_call_id_seq OWNER TO telebot;

--
-- Name: persons_call; Type: TABLE; Schema: public; Owner: telebot
--

CREATE TABLE public.persons_call (
    id integer DEFAULT nextval('public.persons_call_id_seq'::regclass) NOT NULL,
    person_id integer NOT NULL,
    call_name character varying(255) NOT NULL
);


ALTER TABLE public.persons_call OWNER TO telebot;

--
-- Name: persons_id_seq; Type: SEQUENCE; Schema: public; Owner: telebot
--

CREATE SEQUENCE public.persons_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.persons_id_seq OWNER TO telebot;

--
-- Name: persons_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: telebot
--

ALTER SEQUENCE public.persons_id_seq OWNED BY public.persons.id;


--
-- Name: titles; Type: TABLE; Schema: public; Owner: telebot
--

CREATE TABLE public.titles (
    id integer NOT NULL,
    title character varying NOT NULL
);


ALTER TABLE public.titles OWNER TO telebot;

--
-- Name: titles_id_seq; Type: SEQUENCE; Schema: public; Owner: telebot
--

CREATE SEQUENCE public.titles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.titles_id_seq OWNER TO telebot;

--
-- Name: titles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: telebot
--

ALTER SEQUENCE public.titles_id_seq OWNED BY public.titles.id;


--
-- Name: knights id; Type: DEFAULT; Schema: public; Owner: telebot
--

ALTER TABLE ONLY public.knights ALTER COLUMN id SET DEFAULT nextval('public.knights_id_seq'::regclass);


--
-- Name: persons id; Type: DEFAULT; Schema: public; Owner: telebot
--

ALTER TABLE ONLY public.persons ALTER COLUMN id SET DEFAULT nextval('public.persons_id_seq'::regclass);


--
-- Name: titles id; Type: DEFAULT; Schema: public; Owner: telebot
--

ALTER TABLE ONLY public.titles ALTER COLUMN id SET DEFAULT nextval('public.titles_id_seq'::regclass);


--
-- Data for Name: knights; Type: TABLE DATA; Schema: public; Owner: telebot
--

COPY public.knights (id, person_id, title_id) FROM stdin;
1	1	2
2	1	3
3	2	11
4	2	14
5	2	15
6	2	23
7	3	18
8	3	23
9	3	24
12	4	21
15	5	14
13	5	16
14	5	17
16	5	19
17	6	12
18	6	14
19	6	22
21	7	4
22	7	8
20	7	20
\.


--
-- Data for Name: persons; Type: TABLE DATA; Schema: public; Owner: telebot
--

COPY public.persons (id, person, rank_id, user_id, user_name_to_call) FROM stdin;
1	сер Андрій Хмелевовк	1	376412557	@AndriySikora
2	сер Євген Фирмен	5	334776622	@West_Lion
3	сер Олександр Ведмежий Корінь	6	342974404	@Sasha_Korenivsky
4	сер Данило владика Срібного меча	9	299536942	@MonsterLOL
5	сер Іван Доктор Стометрівка	7	376549605	@OscarD
6	сер Данило Саловрот	10	346790305	@noctua_rb
7	леді Марі-Вовчиця Шелест Вогню	13	575505064	@575505064
8	сер Денис Цирюльник	6	401928454	@globalus
9	сер Димитрій Техноварвар з Диванії	13	271837413	@271837413
\.


--
-- Data for Name: persons_call; Type: TABLE DATA; Schema: public; Owner: telebot
--

COPY public.persons_call (id, person_id, call_name) FROM stdin;
38	6	сало
39	6	смалець
40	6	шмалець
41	4	срібний
42	4	срібло
43	4	монтажор
44	5	ваня
45	5	йване
46	5	іван
47	8	дєня
48	8	денис
49	8	денчик
50	8	цирюльник
51	2	жека
52	2	женя
53	2	жекіпше
54	2	фирмен
55	2	батон
56	1	андрюха
57	1	вождь
58	1	бухововк
59	1	хмелевовк
60	7	марі
61	7	марічка
62	3	саша
63	3	саня
64	3	корінь
65	3	саньок
66	3	олександр
67	9	діма
68	9	дімон
69	9	дямон
70	9	техноварвар
\.


--
-- Data for Name: titles; Type: TABLE DATA; Schema: public; Owner: telebot
--

COPY public.titles (id, title) FROM stdin;
1	Його величність
2	магістр ордену ЛКС
3	перший свого імені
4	перша пані ордену
5	Його святість
6	Лицар ордену
7	Каштелян
8	казкар ордену
9	Майстер ордену
10	Почесний Лорд-Командир
11	почесний лорд-інквізитор
12	правиця магістра
13	Послушник ордену
14	один з первоосвячених
15	верховний комісар
16	владика фортеці
17	хранитель заходу
18	непідпалимий
19	володар комірки рижух
20	сержант-інквізитор
21	той що біжить Карпатами
22	той що завів трактор
23	воїн літнього сонця
24	Змієборець
\.


--
-- Name: knights_id_seq; Type: SEQUENCE SET; Schema: public; Owner: telebot
--

SELECT pg_catalog.setval('public.knights_id_seq', 28, true);


--
-- Name: persons_call_id_seq; Type: SEQUENCE SET; Schema: public; Owner: telebot
--

SELECT pg_catalog.setval('public.persons_call_id_seq', 75, true);


--
-- Name: persons_id_seq; Type: SEQUENCE SET; Schema: public; Owner: telebot
--

SELECT pg_catalog.setval('public.persons_id_seq', 28, true);


--
-- Name: titles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: telebot
--

SELECT pg_catalog.setval('public.titles_id_seq', 28, true);


--
-- Name: knights knights_person_id_title_id_key; Type: CONSTRAINT; Schema: public; Owner: telebot
--

ALTER TABLE ONLY public.knights
    ADD CONSTRAINT knights_person_id_title_id_key UNIQUE (person_id, title_id);


--
-- Name: knights knights_pkey; Type: CONSTRAINT; Schema: public; Owner: telebot
--

ALTER TABLE ONLY public.knights
    ADD CONSTRAINT knights_pkey PRIMARY KEY (id);


--
-- Name: persons_call persons_call_person_id_call_name_key; Type: CONSTRAINT; Schema: public; Owner: telebot
--

ALTER TABLE ONLY public.persons_call
    ADD CONSTRAINT persons_call_person_id_call_name_key UNIQUE (person_id, call_name);


--
-- Name: persons_call persons_call_pkey; Type: CONSTRAINT; Schema: public; Owner: telebot
--

ALTER TABLE ONLY public.persons_call
    ADD CONSTRAINT persons_call_pkey PRIMARY KEY (id);


--
-- Name: persons persons_pkey; Type: CONSTRAINT; Schema: public; Owner: telebot
--

ALTER TABLE ONLY public.persons
    ADD CONSTRAINT persons_pkey PRIMARY KEY (id);


--
-- Name: titles titles_pkey; Type: CONSTRAINT; Schema: public; Owner: telebot
--

ALTER TABLE ONLY public.titles
    ADD CONSTRAINT titles_pkey PRIMARY KEY (id);


--
-- Name: person_id; Type: INDEX; Schema: public; Owner: telebot
--

CREATE INDEX person_id ON public.knights USING btree (person_id);


--
-- Name: title_id; Type: INDEX; Schema: public; Owner: telebot
--

CREATE INDEX title_id ON public.knights USING btree (title_id);


--
-- Name: knights fk_person; Type: FK CONSTRAINT; Schema: public; Owner: telebot
--

ALTER TABLE ONLY public.knights
    ADD CONSTRAINT fk_person FOREIGN KEY (person_id) REFERENCES public.persons(id) ON DELETE CASCADE;


--
-- Name: persons_call fk_person_ld; Type: FK CONSTRAINT; Schema: public; Owner: telebot
--

ALTER TABLE ONLY public.persons_call
    ADD CONSTRAINT fk_person_ld FOREIGN KEY (person_id) REFERENCES public.persons(id) ON DELETE CASCADE;


--
-- Name: knights fk_title; Type: FK CONSTRAINT; Schema: public; Owner: telebot
--

ALTER TABLE ONLY public.knights
    ADD CONSTRAINT fk_title FOREIGN KEY (title_id) REFERENCES public.titles(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

