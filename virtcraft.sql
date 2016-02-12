--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: comments; Type: TABLE; Schema: public; Owner: ltaziri; Tablespace: 
--

CREATE TABLE comments (
    comment_id integer NOT NULL,
    comment_text character varying(255) NOT NULL,
    comment_image character varying(255),
    comment_timestamp timestamp without time zone NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE comments OWNER TO ltaziri;

--
-- Name: comments_comment_id_seq; Type: SEQUENCE; Schema: public; Owner: ltaziri
--

CREATE SEQUENCE comments_comment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE comments_comment_id_seq OWNER TO ltaziri;

--
-- Name: comments_comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ltaziri
--

ALTER SEQUENCE comments_comment_id_seq OWNED BY comments.comment_id;


--
-- Name: groups; Type: TABLE; Schema: public; Owner: ltaziri; Tablespace: 
--

CREATE TABLE groups (
    group_id integer NOT NULL,
    group_name character varying(64) NOT NULL,
    group_descrip character varying(255),
    group_image character varying(255) NOT NULL,
    pattern_image character varying(255),
    pattern_link character varying(255),
    pattern_name character varying(255)
);


ALTER TABLE groups OWNER TO ltaziri;

--
-- Name: groups_group_id_seq; Type: SEQUENCE; Schema: public; Owner: ltaziri
--

CREATE SEQUENCE groups_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE groups_group_id_seq OWNER TO ltaziri;

--
-- Name: groups_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ltaziri
--

ALTER SEQUENCE groups_group_id_seq OWNED BY groups.group_id;


--
-- Name: invites; Type: TABLE; Schema: public; Owner: ltaziri; Tablespace: 
--

CREATE TABLE invites (
    invite_id integer NOT NULL,
    invite_email character varying(255) NOT NULL,
    invite_text character varying(255) NOT NULL,
    invite_timestamp timestamp without time zone NOT NULL,
    invite_confirm boolean NOT NULL DEFAULT FALSE,
    group_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE invites OWNER TO ltaziri;

--
-- Name: invites_invite_id_seq; Type: SEQUENCE; Schema: public; Owner: ltaziri
--

CREATE SEQUENCE invites_invite_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE invites_invite_id_seq OWNER TO ltaziri;

--
-- Name: invites_invite_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ltaziri
--

ALTER SEQUENCE invites_invite_id_seq OWNED BY invites.invite_id;


--
-- Name: usergroups; Type: TABLE; Schema: public; Owner: ltaziri; Tablespace: 
--

CREATE TABLE usergroups (
    usergroup_id integer NOT NULL,
    group_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE usergroups OWNER TO ltaziri;

--
-- Name: usergroups_usergroup_id_seq; Type: SEQUENCE; Schema: public; Owner: ltaziri
--

CREATE SEQUENCE usergroups_usergroup_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE usergroups_usergroup_id_seq OWNER TO ltaziri;

--
-- Name: usergroups_usergroup_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ltaziri
--

ALTER SEQUENCE usergroups_usergroup_id_seq OWNED BY usergroups.usergroup_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: ltaziri; Tablespace: 
--

CREATE TABLE users (
    user_id integer NOT NULL,
    email character varying(64) NOT NULL,
    password character varying(64) NOT NULL,
    first_name character varying(64) NOT NULL,
    last_name character varying(64) NOT NULL,
    user_photo character varying(255) NOT NULL,
    user_descrip character varying(255)
);


ALTER TABLE users OWNER TO ltaziri;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: ltaziri
--

CREATE SEQUENCE users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_user_id_seq OWNER TO ltaziri;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ltaziri
--

ALTER SEQUENCE users_user_id_seq OWNED BY users.user_id;


--
-- Name: comment_id; Type: DEFAULT; Schema: public; Owner: ltaziri
--

ALTER TABLE ONLY comments ALTER COLUMN comment_id SET DEFAULT nextval('comments_comment_id_seq'::regclass);


--
-- Name: group_id; Type: DEFAULT; Schema: public; Owner: ltaziri
--

ALTER TABLE ONLY groups ALTER COLUMN group_id SET DEFAULT nextval('groups_group_id_seq'::regclass);


--
-- Name: invite_id; Type: DEFAULT; Schema: public; Owner: ltaziri
--

ALTER TABLE ONLY invites ALTER COLUMN invite_id SET DEFAULT nextval('invites_invite_id_seq'::regclass);


--
-- Name: usergroup_id; Type: DEFAULT; Schema: public; Owner: ltaziri
--

ALTER TABLE ONLY usergroups ALTER COLUMN usergroup_id SET DEFAULT nextval('usergroups_usergroup_id_seq'::regclass);


--
-- Name: user_id; Type: DEFAULT; Schema: public; Owner: ltaziri
--

ALTER TABLE ONLY users ALTER COLUMN user_id SET DEFAULT nextval('users_user_id_seq'::regclass);


--
-- Data for Name: comments; Type: TABLE DATA; Schema: public; Owner: ltaziri
--

COPY comments (comment_id, comment_text, comment_image, comment_timestamp, user_id, group_id) FROM stdin;
1	I love knitting with dog hair!	https://assets.rbl.ms/156392/980x.jpg	2016-02-10 12:09:25.017629	1	1
2	All hail ubermelon!		2016-02-10 12:10:24.596318	1	2
3	Me too!!!!!		2016-02-10 12:11:33.474651	5	1
\.


--
-- Name: comments_comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ltaziri
--

SELECT pg_catalog.setval('comments_comment_id_seq', 3, true);


--
-- Data for Name: groups; Type: TABLE DATA; Schema: public; Owner: ltaziri
--

COPY groups (group_id, group_name, group_descrip, group_image, pattern_image, pattern_link, pattern_name) FROM stdin;
1	Dogs Who Knit		http://3.lushome.com/wp-content/uploads/2013/08/pet-design-ideas-knits-clothes-hat-sweaters-4.jpg	http://ecx.images-amazon.com/images/I/51bY21VdKkL._SX258_BO1,204,203,200_.jpg	http://www.amazon.com/Knitting-With-Dog-Hair-Sweater/dp/0312152906	Knit with Dog Hair
2	Ubermelon Knitters		http://thumbs.dreamstime.com/z/funny-young-pretty-female-helmet-fresh-melon-22528517.jpg	https://img0.etsystatic.com/042/0/6907023/il_570xN.648189754_ameg.jpg	https://www.etsy.com/listing/202036252/water-melon-beanie-hand-knit-hat-women	Watermelon Hat
3	Crazy Dog Lady Sewing Challenge		https://farm8.staticflickr.com/7648/16876119351_15c7ca5007_z.jpg	http://cdn3.craftsy.com/blog/wp-content/uploads/2014/07/full_6402_23311_SammyBagDogSling_2.jpg	http://www.craftsy.com/blog/2014/08/patterns-to-sew-for-dogs/	Dog Carrier
\.


--
-- Name: groups_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ltaziri
--

SELECT pg_catalog.setval('groups_group_id_seq', 4, true);


--
-- Data for Name: invites; Type: TABLE DATA; Schema: public; Owner: ltaziri
--

COPY invites (invite_id, invite_email, invite_text, invite_timestamp, invite_confirm, group_id, user_id) FROM stdin;
2	ltaziri@gmail.com	Hey! I'd love for you to join my rad group!	2016-02-11 14:35:36.889184	FALSE   1	1
\.


--
-- Name: invites_invite_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ltaziri
--

SELECT pg_catalog.setval('invites_invite_id_seq', 7, true);


--
-- Data for Name: usergroups; Type: TABLE DATA; Schema: public; Owner: ltaziri
--

COPY usergroups (usergroup_id, group_id, user_id) FROM stdin;
1	1	1
2	2	1
3	3	1
4	2	5
5	2	3
6	2	7
7	2	30
8	2	19
9	2	6
10	2	8
11	3	5
12	3	3
13	3	15
14	3	11
15	3	8
16	3	9
17	3	13
18	1	5
19	1	7
20	1	19
21	1	6
\.


--
-- Name: usergroups_usergroup_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ltaziri
--

SELECT pg_catalog.setval('usergroups_usergroup_id_seq', 1, false);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: ltaziri
--

COPY users (user_id, email, password, first_name, last_name, user_photo, user_descrip) FROM stdin;
2	katie@hbmail.com	test	Katie	Atkinson	http://thumbs.dreamstime.com/z/mujer-de-costura-50670313.jpg	
3	annie@hbmail.com	test	Annie	He	http://thumbs.dreamstime.com/z/craft-woman-crafter-scissors-glue-gun-50670500.jpg	
4	alena@hbmail.com	test	Alena	Kruchkova	http://thumbs.dreamstime.com/z/sewing-crafting-woman-crafter-machine-50670444.jpg	
5	terri@hbmail.com	test	Terri	Wong	http://thumbs.dreamstime.com/z/mujer-de-costura-50670313.jpg	
6	kara@hbmail.com	test	Kara	Yount	http://thumbs.dreamstime.com/z/craft-woman-crafter-scissors-glue-gun-50670500.jpg	
7	erin@hbmail.com	test	Erin	Allard	http://thumbs.dreamstime.com/z/sewing-crafting-woman-crafter-machine-50670444.jpg	
8	chelsea@hbmail.com	test	Chelsea	Little	http://thumbs.dreamstime.com/z/mujer-de-costura-50670313.jpg	
9	alice@hbmail.com	test	Alice	Pao	http://thumbs.dreamstime.com/z/craft-woman-crafter-scissors-glue-gun-50670500.jpg	
10	shai@hbmail.com	test	Shai	Wilson	http://thumbs.dreamstime.com/z/sewing-crafting-woman-crafter-machine-50670444.jpg	
11	alitsiya@hbmail.com	test	Alitsiya	Yusupova	http://thumbs.dreamstime.com/z/mujer-de-costura-50670313.jpg	
12	patricia@hbmail.com	test	Patrica	Arbona	http://thumbs.dreamstime.com/z/craft-woman-crafter-scissors-glue-gun-50670500.jpg	
13	emma@hbmail.com	test	Emma	Ferguson	http://thumbs.dreamstime.com/z/sewing-crafting-woman-crafter-machine-50670444.jpg	
14	bekka@hbmail.com	test	Bekka	Murphy	http://thumbs.dreamstime.com/z/mujer-de-costura-50670313.jpg	
15	celia@hbmail.com	test	Celia	Waggoner	http://thumbs.dreamstime.com/z/craft-woman-crafter-scissors-glue-gun-50670500.jpg	
16	elsa@hbmail.com	test	Elsa	Birch	http://thumbs.dreamstime.com/z/sewing-crafting-woman-crafter-machine-50670444.jpg	
17	kaylie@hbmail.com	test	Kaylie	Kwon	http://thumbs.dreamstime.com/z/mujer-de-costura-50670313.jpg	
18	emily@hbmail.com	test	Emily	Lam	http://thumbs.dreamstime.com/z/craft-woman-crafter-scissors-glue-gun-50670500.jpg	
19	vianey@hbmail.com	test	Vianey	Munoz Gallegos	http://thumbs.dreamstime.com/z/sewing-crafting-woman-crafter-machine-50670444.jpg	
20	marisha@hbmail.com	test	Marisha	Schumacher-Hodge	http://thumbs.dreamstime.com/z/mujer-de-costura-50670313.jpg	
21	anli@hbmail.com	test	Anli	Yang	http://thumbs.dreamstime.com/z/craft-woman-crafter-scissors-glue-gun-50670500.jpg	
22	chandrika@hbmail.com	test	Chandrika	Achar	http://thumbs.dreamstime.com/z/sewing-crafting-woman-crafter-machine-50670444.jpg	
23	meg@hbmail.com	test	Meg	Bishop	http://thumbs.dreamstime.com/z/mujer-de-costura-50670313.jpg	
24	tiffany@hbmail.com	test	Tiffany	Hakseth	http://thumbs.dreamstime.com/z/craft-woman-crafter-scissors-glue-gun-50670500.jpg	
25	megan@hbmail.com	test	Megan	Peterson	http://thumbs.dreamstime.com/z/sewing-crafting-woman-crafter-machine-50670444.jpg	
26	shalini@hbmail.com	test	Shalini	Pyapali	http://thumbs.dreamstime.com/z/mujer-de-costura-50670313.jpg	
27	dori@hbmail.com	test	Dori	Runyon	http://thumbs.dreamstime.com/z/craft-woman-crafter-scissors-glue-gun-50670500.jpg	
28	melissa@hbmail.com	test	Melissa	Fabros	http://thumbs.dreamstime.com/z/sewing-crafting-woman-crafter-machine-50670444.jpg	
29	shijie@hbmail.com	test	Shijie	Feng	http://thumbs.dreamstime.com/z/mujer-de-costura-50670313.jpg	
30	janet@hbmail.com	test	Janet	Ghazizadeh	http://thumbs.dreamstime.com/z/craft-woman-crafter-scissors-glue-gun-50670500.jpg	
31	doria@hbmail.com	test	Doria	Keung	http://thumbs.dreamstime.com/z/sewing-crafting-woman-crafter-machine-50670444.jpg	
32	malika@hbmail.com	test	Malika	Nikhmonova	http://thumbs.dreamstime.com/z/mujer-de-costura-50670313.jpg	
33	allian@hbmail.com	test	Allian	Roman	http://thumbs.dreamstime.com/z/craft-woman-crafter-scissors-glue-gun-50670500.jpg	
34	florence@hbmail.com	test	Florence	Loi	http://thumbs.dreamstime.com/z/sewing-crafting-woman-crafter-machine-50670444.jpg	
35	kristin@hbmail.com	test	Kristin	Parke	http://thumbs.dreamstime.com/z/mujer-de-costura-50670313.jpg	
1	leilani@hbmail.com	test	Leilani	Taziri	http://thumbs.dreamstime.com/z/sewing-crafting-woman-crafter-machine-50670444.jpg	My name is Leilani and I love to knit!!!!!!!!!!!!!!
\.


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ltaziri
--

SELECT pg_catalog.setval('users_user_id_seq', 36, true);


--
-- Name: comments_pkey; Type: CONSTRAINT; Schema: public; Owner: ltaziri; Tablespace: 
--

ALTER TABLE ONLY comments
    ADD CONSTRAINT comments_pkey PRIMARY KEY (comment_id);


--
-- Name: groups_pkey; Type: CONSTRAINT; Schema: public; Owner: ltaziri; Tablespace: 
--

ALTER TABLE ONLY groups
    ADD CONSTRAINT groups_pkey PRIMARY KEY (group_id);


--
-- Name: invites_pkey; Type: CONSTRAINT; Schema: public; Owner: ltaziri; Tablespace: 
--

ALTER TABLE ONLY invites
    ADD CONSTRAINT invites_pkey PRIMARY KEY (invite_id);


--
-- Name: usergroups_pkey; Type: CONSTRAINT; Schema: public; Owner: ltaziri; Tablespace: 
--

ALTER TABLE ONLY usergroups
    ADD CONSTRAINT usergroups_pkey PRIMARY KEY (usergroup_id);


--
-- Name: users_email_key; Type: CONSTRAINT; Schema: public; Owner: ltaziri; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: ltaziri; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: comments_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ltaziri
--

ALTER TABLE ONLY comments
    ADD CONSTRAINT comments_group_id_fkey FOREIGN KEY (group_id) REFERENCES groups(group_id);


--
-- Name: comments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ltaziri
--

ALTER TABLE ONLY comments
    ADD CONSTRAINT comments_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: invites_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ltaziri
--

ALTER TABLE ONLY invites
    ADD CONSTRAINT invites_group_id_fkey FOREIGN KEY (group_id) REFERENCES groups(group_id);


--
-- Name: invites_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ltaziri
--

ALTER TABLE ONLY invites
    ADD CONSTRAINT invites_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: usergroups_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ltaziri
--

ALTER TABLE ONLY usergroups
    ADD CONSTRAINT usergroups_group_id_fkey FOREIGN KEY (group_id) REFERENCES groups(group_id);


--
-- Name: usergroups_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ltaziri
--

ALTER TABLE ONLY usergroups
    ADD CONSTRAINT usergroups_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: public; Type: ACL; Schema: -; Owner: ltaziri
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM ltaziri;
GRANT ALL ON SCHEMA public TO ltaziri;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

