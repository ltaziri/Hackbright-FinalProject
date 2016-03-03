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
    admin_id integer NOT NULL,
    vote_timestamp timestamp without time zone,
    vote_days integer,
    hashtag character varying(64)
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
    invite_confirm boolean NOT NULL,
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
-- Name: patterns; Type: TABLE; Schema: public; Owner: ltaziri; Tablespace: 
--

CREATE TABLE patterns (
    pattern_id integer NOT NULL,
    pattern_name character varying(255) NOT NULL,
    pattern_link character varying(255),
    pattern_pdf character varying(255),
    chosen boolean NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE patterns OWNER TO ltaziri;

--
-- Name: patterns_pattern_id_seq; Type: SEQUENCE; Schema: public; Owner: ltaziri
--

CREATE SEQUENCE patterns_pattern_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE patterns_pattern_id_seq OWNER TO ltaziri;

--
-- Name: patterns_pattern_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ltaziri
--

ALTER SEQUENCE patterns_pattern_id_seq OWNED BY patterns.pattern_id;


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
-- Name: votes; Type: TABLE; Schema: public; Owner: ltaziri; Tablespace: 
--

CREATE TABLE votes (
    group_id integer NOT NULL,
    user_id integer NOT NULL,
    pattern_id integer NOT NULL
);


ALTER TABLE votes OWNER TO ltaziri;

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
-- Name: pattern_id; Type: DEFAULT; Schema: public; Owner: ltaziri
--

ALTER TABLE ONLY patterns ALTER COLUMN pattern_id SET DEFAULT nextval('patterns_pattern_id_seq'::regclass);


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
1		static/images/balloonicorn_1_1_1_1_1_1_1_2.jpg	2016-02-25 22:01:01.837574	1	1
2	still working?	\N	2016-02-27 09:55:48.948407	1	1
3	test	\N	2016-02-27 10:12:47.91283	1	1
4	test	\N	2016-02-27 10:13:00.077278	1	3
5		static/images/balloonicorn_1_1_1_1_1_1_1_2_1.jpg	2016-02-27 10:13:16.977137	1	3
6	test	\N	2016-02-27 10:19:03.08055	1	1
7	retest	\N	2016-02-27 11:37:21.651195	1	3
8	test	\N	2016-03-01 14:27:24.93971	1	9
9	http://stackoverflow.com/	\N	2016-03-01 14:49:07.770261	1	9
10	http://stackoverflow.com/	\N	2016-03-01 15:08:34.300031	1	9
11	http://stackoverflow.com/	\N	2016-03-01 15:12:12.22949	1	9
12	http://stackoverflow.com/	\N	2016-03-01 15:15:41.535915	1	9
13	http://stackoverflow.com/	\N	2016-03-01 15:15:51.798894	1	9
14	http://stackoverflow.com/NEW	\N	2016-03-01 15:16:06.134892	1	9
15		static/images/tiger_1_1_1_1_1_1.jpeg	2016-03-01 15:16:52.467849	1	9
16		static/images/balloonicorn_1_1_1_1_1_1_1_1_1_1.jpg	2016-03-01 15:18:19.499865	1	9
17		\N	2016-03-01 15:18:25.014087	1	9
18		\N	2016-03-01 15:21:48.574481	1	9
19		\N	2016-03-01 15:24:23.812045	1	9
20		\N	2016-03-01 15:25:39.905137	1	9
21	Test	\N	2016-03-01 15:31:03.090411	1	9
22	http://stackoverflow.com/	\N	2016-03-01 15:39:41.655984	1	2
23	test	\N	2016-03-01 16:09:21.123686	1	9
24		\N	2016-03-01 16:17:16.979305	1	9
25		\N	2016-03-01 16:17:21.845913	1	9
26	test	\N	2016-03-01 16:33:55.935663	1	9
27		static/images/tiger_1_1_1_1_1_1_1.jpeg	2016-03-01 16:51:09.260917	1	1
28		static/images/balloonicorn_1_1_1_1_1_1_1_1_1_1_1.jpg	2016-03-01 16:51:49.805445	1	1
29		static/images/tiger_1_1_1_1_1_1_1_1.jpeg	2016-03-01 19:39:25.952676	1	1
30		static/images/balloonicorn_1_1_1_1_1_1_1_1_1_1_2.jpg	2016-03-01 19:39:40.540812	1	1
31		static/images/sewing_tweet_pic2.jpg	2016-03-01 22:41:35.839689	1	1
32		static/images/sewing_tweet_pic2_1.jpg	2016-03-01 22:41:50.60214	1	1
33		\N	2016-03-01 22:41:57.146912	1	1
34		static/images/sewing_tweet_pic1.jpg	2016-03-01 22:42:05.91512	1	1
35	test	\N	2016-03-02 17:11:51.670018	1	1
36	http://www.w3schools.com/html/html_youtube.asp	\N	2016-03-02 17:14:16.664147	1	1
37	http://www.w3schools.com/html/html_youtube.asp	\N	2016-03-02 17:14:35.741067	1	1
38	test	\N	2016-03-02 17:14:58.798343	1	1
39	test	\N	2016-03-02 17:16:03.670198	1	1
40	http://www.w3schools.com/html/html_youtube.asp	\N	2016-03-02 17:16:16.1041	1	1
41	www.test.com	\N	2016-03-02 18:09:05.342393	1	1
42	I am testing a bunch of text with some links thrown in http://www.sometest.com	\N	2016-03-02 21:02:54.062843	1	1
43	I am testing a bunch of text with some links thrown in http://www.sometest.com	\N	2016-03-02 21:04:09.748924	1	1
44	Testing with a youtube link	\N	2016-03-02 21:07:12.060016	1	1
45	Testing with a youtube https://www.youtube.com/watch?v=Exf8RbgKmhM link	\N	2016-03-02 21:07:42.469009	1	1
46	Testing text with youtube https://www.youtube.com/watch?v=5yT2dQoCo4Y	\N	2016-03-02 21:58:30.788698	1	1
47	testi without youtube	\N	2016-03-02 22:01:41.659522	1	1
48	Testing text with youtube https://www.youtube.com/watch?v=5yT2dQoCo4Y	\N	2016-03-02 22:12:36.179643	1	1
49	Testing text with youtube https://www.youtube.com/watch?v=5yT2dQoCo4Y	\N	2016-03-02 22:13:52.625416	1	1
50	Testing text with youtube https://www.youtube.com/watch?v=5yT2dQoCo4Y	\N	2016-03-02 22:14:16.290236	1	1
51	Testing text with youtube https://www.youtube.com/watch?v=5yT2dQoCo4Y	\N	2016-03-02 22:14:35.064289	1	1
52	Testing text with youtube https://www.youtube.com/watch?v=5yT2dQoCo4Y	\N	2016-03-02 22:16:49.261428	1	1
53	Testing text with youtube https://www.youtube.com/watch?v=5yT2dQoCo4Y	\N	2016-03-02 22:22:27.730078	1	1
54	esting text with youtube https://www.youtube.com/watch?v=5yT2dQoCo4Y	\N	2016-03-02 22:23:30.326038	1	1
55	esting text with youtube https://www.youtube.com/watch?v=5yT2dQoCo4Y	\N	2016-03-02 22:24:08.024979	1	1
56	esting text with youtube https://www.youtube.com/watch?v=5yT2dQoCo4Y	\N	2016-03-02 22:25:00.548154	1	1
57	esting text with youtube https://www.youtube.com/watch?v=5yT2dQoCo4Y	\N	2016-03-02 22:25:18.438419	1	1
58	https://www.youtube.com/watch?v=bhDrDRVjCqg	\N	2016-03-02 22:26:25.427138	1	1
59	https://www.youtube.com/watch?v=bhDrDRVjCqg	\N	2016-03-02 22:28:41.529983	1	1
\.


--
-- Name: comments_comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ltaziri
--

SELECT pg_catalog.setval('comments_comment_id_seq', 59, true);


--
-- Data for Name: groups; Type: TABLE DATA; Schema: public; Owner: ltaziri
--

COPY groups (group_id, group_name, group_descrip, group_image, admin_id, vote_timestamp, vote_days, hashtag) FROM stdin;
3	Cricut Crafters - Earrings		static/images/craft_group_default.jpg	1	\N	\N	#makealongcricutcraftersfeb
2	Super Sewers		static/images/sewing_group_default.jpg	1	\N	\N	#makealongsupersewers
8	testing	Lets try to add something to our test group	static/images/sewing_group_default.jpg	1	2016-02-27 17:54:47.022961	3	#makealongtestagain
7	Testing 	test	static/images/tiger_1_1_1_1_1.jpeg	1	\N	\N	\N
11	New Group	Tesst	static/images/knitting_group_default.jpg	1	\N	\N	#makealongtetakj
12	test agaom	group without pattern pdf	static/images/craft_group_default.jpg	1	\N	\N	#makealong
13	Test with Poll	trying our helper function with poll	static/images/balloonicorn_1_1_1_1_1_1_1_1_1.jpg	1	2016-02-29 15:36:17.434472	3	#makealong
10	New Group	Tesst	static/images/knitting_group_default.jpg	1	2016-02-29 16:06:24.717987	5	#makealongtetakj
14	Test		static/images/craft_group_default.jpg	1	2016-02-29 17:02:56.154132	2	#makealong
16	test test test		static/images/knitting_group_default.jpg	1	2016-02-29 17:20:35.629755	2	#makealong
15	NEED TO FIND THIS ONE TOO!		static/images/craft_group_default.jpg	1	2016-02-29 17:05:48.910569	2	#makealong
1	Knitters to the rescue!	www.test.com	static/images/knitting_group_default.jpg	1	2016-03-02 00:00:00	7	#makealongknittersrescue
9	testing 	Tesst	static/images/knitting_group_default.jpg	1	2016-02-29 17:37:41.092818	2	#makealongtetakj
\.


--
-- Name: groups_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ltaziri
--

SELECT pg_catalog.setval('groups_group_id_seq', 16, true);


--
-- Data for Name: invites; Type: TABLE DATA; Schema: public; Owner: ltaziri
--

COPY invites (invite_id, invite_email, invite_text, invite_timestamp, invite_confirm, group_id, user_id) FROM stdin;
1	ltaziri@gmail.com	YO!	2016-03-02 16:17:13.177956	f	1	1
2	ltaziri@gmail.com	YO!	2016-03-02 18:36:53.90941	f	1	1
\.


--
-- Name: invites_invite_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ltaziri
--

SELECT pg_catalog.setval('invites_invite_id_seq', 2, true);


--
-- Data for Name: patterns; Type: TABLE DATA; Schema: public; Owner: ltaziri
--

COPY patterns (pattern_id, pattern_name, pattern_link, pattern_pdf, chosen, group_id) FROM stdin;
1	Killgore Mitts	https://www.fancytigercrafts.com/patterns/fancy-tiger-crafts/kilgore-mitts	static/pdfs/kilgore_mits.pdf	f	1
2	Exeter	http://www.ravelry.com/patterns/library/exeter-2	static/pdfs/Exeter5.pdf	f	1
3	I Heart Cables	http://www.ravelry.com/patterns/library/i-heart-cables	static/pdfs/I_Heart_Cables.pdf	f	1
16	pattern2		static/pdfs/3245_instructions_1_4.pdf	f	8
17	pattern3		\N	f	8
18	New Pattern	http://www.sometest.com	\N	t	7
15	pattern1		\N	t	8
19	Test Pattern		static/pdfs/3245_instructions_1_3_1.pdf	t	11
20	some pattern	http://www.amazon.com/Knitting-With-Dog-Hair-Sweater/dp/0312152906	\N	t	12
21	Pattern 1		\N	t	13
22			static/pdfs/3245_instructions_1_4_1.pdf	t	13
23		http://test.pattern.com	\N	t	13
24	First Pattern		\N	t	10
25	Second Pattern		\N	t	10
26	Third pattern		\N	t	10
29	Test1		\N	t	16
30	Test2		\N	t	16
34	Test Pattern		\N	t	2
31	Test1		\N	f	9
33	Test 3		static/pdfs/3245_instructions_1_3_2.pdf	f	9
32	Test2	http://www.test.com	\N	t	9
27	Test1		\N	f	15
28	Test2	http://www.test.com	\N	t	15
\.


--
-- Name: patterns_pattern_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ltaziri
--

SELECT pg_catalog.setval('patterns_pattern_id_seq', 34, true);


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
25	7	1
26	8	1
27	9	1
28	10	1
29	11	1
30	12	1
31	13	1
32	15	1
33	16	1
\.


--
-- Name: usergroups_usergroup_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ltaziri
--

SELECT pg_catalog.setval('usergroups_usergroup_id_seq', 33, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: ltaziri
--

COPY users (user_id, email, password, first_name, last_name, user_photo, user_descrip) FROM stdin;
2	katie@hbmail.com	test	Katie	Atkinson	static/images/glue_gun.jpg	
3	annie@hbmail.com	test	Annie	He	static/images/crafter.jpg	
4	alena@hbmail.com	test	Alena	Kruchkova	static/images/crafter.jpg	
5	terri@hbmail.com	test	Terri	Wong	static/images/glue_gun.jpg	
6	kara@hbmail.com	test	Kara	Yount	static/images/sewing_machine.jpg	
7	erin@hbmail.com	test	Erin	Allard	static/images/crafter.jpg	
8	chelsea@hbmail.com	test	Chelsea	Little	static/images/glue_gun.jpg	
9	alice@hbmail.com	test	Alice	Pao	static/images/sewing_machine.jpg	
10	shai@hbmail.com	test	Shai	Wilson	static/images/crafter.jpg	
11	alitsiya@hbmail.com	test	Alitsiya	Yusupova	static/images/glue_gun.jpg	
12	patricia@hbmail.com	test	Patrica	Arbona	static/images/sewing_machine.jpg	
13	emma@hbmail.com	test	Emma	Ferguson	static/images/crafter.jpg	
14	bekka@hbmail.com	test	Bekka	Murphy	static/images/glue_gun.jpg	
15	celia@hbmail.com	test	Celia	Waggoner	static/images/sewing_machine.jpg	
16	elsa@hbmail.com	test	Elsa	Birch	static/images/crafter.jpg	
17	kaylie@hbmail.com	test	Kaylie	Kwon	static/images/glue_gun.jpg	
18	emily@hbmail.com	test	Emily	Lam	static/images/sewing_machine.jpg	
19	vianey@hbmail.com	test	Vianey	Munoz Gallegos	static/images/crafter.jpg	
20	marisha@hbmail.com	test	Marisha	Schumacher-Hodge	static/images/glue_gun.jpg	
21	anli@hbmail.com	test	Anli	Yang	static/images/sewing_machine.jpg	
22	chandrika@hbmail.com	test	Chandrika	Achar	static/images/crafter.jpg	
23	meg@hbmail.com	test	Meg	Bishop	static/images/glue_gun.jpg	
24	tiffany@hbmail.com	test	Tiffany	Hakseth	static/images/sewing_machine.jpg	
25	megan@hbmail.com	test	Megan	Peterson	static/images/crafter.jpg	
26	shalini@hbmail.com	test	Shalini	Pyapali	static/images/glue_gun.jpg	
27	dori@hbmail.com	test	Dori	Runyon	static/images/sewing_machine.jpg	
28	melissa@hbmail.com	test	Melissa	Fabros	static/images/crafter.jpg	
29	shijie@hbmail.com	test	Shijie	Feng	static/images/glue_gun.jpg	
30	janet@hbmail.com	test	Janet	Ghazizadeh	static/images/sewing_machine.jpg	
31	doria@hbmail.com	test	Doria	Keung	static/images/crafter.jpg	
32	malika@hbmail.com	test	Malika	Nikhmonova	static/images/glue_gun.jpg	
33	allian@hbmail.com	test	Allian	Roman	static/images/sewing_machine.jpg	
34	florence@hbmail.com	test	Florence	Loi	static/images/crafter.jpg	
35	kristin@hbmail.com	test	Kristin	Parke	static/images/glue_gun.jpg	
1	leilani@hbmail.com	test	Leilani	Taziri	static/images/profilepic_2_1.jpg	                
37	new@hbmail.com	test	test	test	static/images/glue_gun.jpg	\N
38	leilani	test	lt	taz	static/images/crafter.jpg	\N
\.


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ltaziri
--

SELECT pg_catalog.setval('users_user_id_seq', 38, true);


--
-- Data for Name: votes; Type: TABLE DATA; Schema: public; Owner: ltaziri
--

COPY votes (group_id, user_id, pattern_id) FROM stdin;
1	1	1
8	1	16
9	1	32
15	1	28
\.


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
-- Name: patterns_pkey; Type: CONSTRAINT; Schema: public; Owner: ltaziri; Tablespace: 
--

ALTER TABLE ONLY patterns
    ADD CONSTRAINT patterns_pkey PRIMARY KEY (pattern_id);


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
-- Name: votes_pkey; Type: CONSTRAINT; Schema: public; Owner: ltaziri; Tablespace: 
--

ALTER TABLE ONLY votes
    ADD CONSTRAINT votes_pkey PRIMARY KEY (group_id, user_id);


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
-- Name: groups_admin_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ltaziri
--

ALTER TABLE ONLY groups
    ADD CONSTRAINT groups_admin_id_fkey FOREIGN KEY (admin_id) REFERENCES users(user_id);


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
-- Name: patterns_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ltaziri
--

ALTER TABLE ONLY patterns
    ADD CONSTRAINT patterns_group_id_fkey FOREIGN KEY (group_id) REFERENCES groups(group_id);


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
-- Name: votes_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ltaziri
--

ALTER TABLE ONLY votes
    ADD CONSTRAINT votes_group_id_fkey FOREIGN KEY (group_id) REFERENCES groups(group_id);


--
-- Name: votes_pattern_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ltaziri
--

ALTER TABLE ONLY votes
    ADD CONSTRAINT votes_pattern_id_fkey FOREIGN KEY (pattern_id) REFERENCES patterns(pattern_id);


--
-- Name: votes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ltaziri
--

ALTER TABLE ONLY votes
    ADD CONSTRAINT votes_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


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

