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
    youtube_id character varying(255),
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

COPY comments (comment_id, comment_text, comment_image, comment_timestamp, youtube_id, user_id, group_id) FROM stdin;
19	Can't wait to get started! Anyone want to go to Imagiknit this weekend?	\N	2016-03-03 13:20:39.920426	\N	5	1
20	I am getting started today with some yarn I have in the stash! Testing the gauge as we speak:)	static/images/starting_1_1.jpg	2016-03-03 13:22:12.658793	\N	6	1
21	I am partially through the first mitt. LOVING this Blue Sky cotton yarn	static/images/Killgore_1_1.jpg	2016-03-03 13:28:40.657715	\N	1	1
22	Anyone else having problems with the make one left, make one right combo? I can't get it to look right:(	\N	2016-03-03 13:29:49.892303	\N	7	1
23	@Erin I am having issues too! I feel like the combo should be reversed?	\N	2016-03-03 13:31:32.242097	\N	19	1
25	I followed that make one video and it worked like a charm! Finished my first mitten!	static/images/killgore_2_1.jpg	2016-03-03 13:37:26.680141	\N	5	1
26	OMG Terri your mitten looks great! Love the color!!	\N	2016-03-03 13:38:27.694905	\N	6	1
27	BTW I finished both my mittens this weekend! Moving on to a second pair...	static/images/kilgore_3_2.jpg	2016-03-03 13:39:49.818031	\N	6	1
187	If you are struggling with the make one left/make one right. Here is a video that might help! <a href='https://www.youtube.com/watch?v=nkOwLvcG7m8'>https://www.youtube.com/watch?v=nkOwLvcG7m8</a>	\N	2016-06-01 15:09:25.876682	nkOwLvcG7m8	37	1
\.


--
-- Name: comments_comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ltaziri
--

SELECT pg_catalog.setval('comments_comment_id_seq', 187, true);


--
-- Data for Name: groups; Type: TABLE DATA; Schema: public; Owner: ltaziri
--

COPY groups (group_id, group_name, group_descrip, group_image, admin_id, vote_timestamp, vote_days, hashtag) FROM stdin;
2	Super Sewers	Hey all! So excited to get this month's group going. I have picked three fun Jailie patterns for us to pick from this month!	static/images/sewing_group_default.jpg	37	2016-06-01 15:03:07.973596	7	#makealongsupersewers
5	Women Who Build	Here are three awesome Ana White console wood working plans to choose from.	static/images/wood_1.jpg	1	2016-06-01 15:03:07.982495	7	#makealongwomenwhobuild
3	Crazy Cards - March		static/images/papercrafting_scaled_1_1.jpg	5	\N	\N	#makealongcricutcraftersfeb
1	Knitters to the Rescue!	This month we are working on the Kilgore Mitts pattern.	static/images/knitting_group_default.jpg	1	2016-03-01 00:00:00	1	#makealongknittersrescue
6	Eat. Sleep. Knit.	This is so fun	static/images/knit2_scaled_1.jpg	1	\N	\N	eatsleepknit
7	Crochet All Night!	 	static/images/Crochet_1.jpg	1	\N	\N	#makealongcrochetallnight
10	Test	test	static/images/knitting_group_default.jpg	1	\N	\N	\N
9	Crazy Cards		static/images/papercrafting_scaled_1_1_1.jpg	5	\N	\N	\N
\.


--
-- Name: groups_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ltaziri
--

SELECT pg_catalog.setval('groups_group_id_seq', 11, true);


--
-- Data for Name: invites; Type: TABLE DATA; Schema: public; Owner: ltaziri
--

COPY invites (invite_id, invite_email, invite_text, invite_timestamp, invite_confirm, group_id, user_id) FROM stdin;
70	ltaziri@gmail.com	This is an awesome group! Would love for you to join!	2016-03-12 14:59:16.748542	f	1	1
71	ltaziri@gmail.com	This is an awesome group! Would love for you to join!	2016-03-12 15:09:01.650971	f	1	1
72	ltaziri@gmail.com	This is an awesome group! Would love for you to join!	2016-03-12 15:16:01.480411	f	1	1
40	friend@gmail.com	This is an awesome group! Would love for you to join!	2016-03-07 17:08:01.368071	f	1	1
73	ltaziri@gmail.com	This is an awesome group! Would love for you to join!	2016-03-12 15:21:39.507655	f	1	1
74	ltaziri@gmail.com	This is an awesome group! Would love for you to join!	2016-03-16 20:40:17.02396	f	1	1
3	leilani@hbmail.com	Please join our crafty craft group!	2016-03-03 13:20:39.920426	f	9	5
75	ltaziri@gmail.com	This is an awesome group! Would love for you to join!	2016-04-03 22:25:43.628448	f	1	1
76	demo@makealong.com	This is an awesome group! Would love for you to join!	2016-03-12 14:59:16.748542	f	9	1
\.


--
-- Name: invites_invite_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ltaziri
--

SELECT pg_catalog.setval('invites_invite_id_seq', 76, true);


--
-- Data for Name: patterns; Type: TABLE DATA; Schema: public; Owner: ltaziri
--

COPY patterns (pattern_id, pattern_name, pattern_link, pattern_pdf, chosen, group_id) FROM stdin;
2	Exeter	http://www.ravelry.com/patterns/library/exeter-2	static/pdfs/Exeter5.pdf	f	1
3	I Heart Cables	http://www.ravelry.com/patterns/library/i-heart-cables	static/pdfs/I_Heart_Cables.pdf	f	1
1	Killgore Mitts	https://www.fancytigercrafts.com/patterns/fancy-tiger-crafts/kilgore-mitts	static/pdfs/kilgore_mits.pdf	t	1
5	Scarf Pattern Top	https://jalie.com/jalie2921-scarf-collar-top-sewing-pattern-402	\N	f	2
10	Breakfast Bar Console	http://www.ana-white.com/2016/02/free_plans/40-breakfast-bar-featuring-i-am-homemaker	\N	f	5
9	Rustic X Console	http://www.ana-white.com/2012/05/plans/rustic-x-console	\N	f	5
7	Basic Sweatshirt	https://jalie.com/jalie3355-sweatshirt-hoodie-sweat-pants-pattern	\N	f	2
8	Apothecary Console With Storage	http://www.ana-white.com/2012/03/apothecary-console-storage-doors	static/pdfs/kilgore_mits.pdf	f	5
6	Baseball Tunic Tank	https://jalie.com/jalie3245-raglan-tee-racerback-tank-tunic-pattern	static/pdfs/kilgore_mits.pdf	f	2
\.


--
-- Name: patterns_pattern_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ltaziri
--

SELECT pg_catalog.setval('patterns_pattern_id_seq', 11, true);


--
-- Data for Name: usergroups; Type: TABLE DATA; Schema: public; Owner: ltaziri
--

COPY usergroups (usergroup_id, group_id, user_id) FROM stdin;
1	1	1
2	2	1
83	9	5
4	2	5
5	2	3
6	2	7
7	2	30
8	2	19
9	2	6
10	2	8
84	9	3
85	9	7
86	9	12
87	9	16
18	1	5
19	1	7
20	1	19
21	1	6
25	5	1
26	5	2
27	5	3
28	5	4
29	5	5
102	1	37
103	2	37
104	5	37
105	6	37
43	6	1
44	7	1
106	7	37
\.


--
-- Name: usergroups_usergroup_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ltaziri
--

SELECT pg_catalog.setval('usergroups_usergroup_id_seq', 107, true);


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
1	leilani@hbmail.com	test	Leilani	Taziri	static/images/profilepic_1_1.jpg	 
37	demo@makealong.com	trydemo	Maddy	Maker	static/images/glue_gun.jpg	Maker of anything and everything!
\.


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ltaziri
--

SELECT pg_catalog.setval('users_user_id_seq', 37, true);


--
-- Data for Name: votes; Type: TABLE DATA; Schema: public; Owner: ltaziri
--

COPY votes (group_id, user_id, pattern_id) FROM stdin;
1	1	1
1	6	1
1	5	3
5	2	9
5	3	10
5	4	9
5	5	8
2	1	7
2	5	6
2	3	5
2	7	5
2	30	7
2	19	6
2	6	6
2	8	7
2	37	7
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

