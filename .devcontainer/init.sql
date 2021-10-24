--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.19
-- Dumped by pg_dump version 9.6.19

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
-- Name: application_votes; Type: TABLE; Schema: public; Owner: bot
--

CREATE TABLE public.application_votes (
    id integer NOT NULL,
    applications_id integer,
    discord_user_id bigint,
    is_yes boolean
);


ALTER TABLE public.application_votes OWNER TO bot;

--
-- Name: application_votes_id_seq; Type: SEQUENCE; Schema: public; Owner: bot
--

CREATE SEQUENCE public.application_votes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.application_votes_id_seq OWNER TO bot;

--
-- Name: application_votes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bot
--

ALTER SEQUENCE public.application_votes_id_seq OWNED BY public.application_votes.id;


--
-- Name: applications; Type: TABLE; Schema: public; Owner: bot
--

CREATE TABLE public.applications (
    id integer NOT NULL,
    enjin_app_id integer,
    time_created timestamp with time zone,
    enjin_user_id integer,
    user_ip text,
    enjin_username text,
    age text,
    time_zone text,
    is_wednesday boolean,
    is_friday boolean,
    is_saturday boolean,
    steam_profile text,
    referral text,
    reason text,
    message_id bigint,
    is_approved boolean,
    is_message_sent boolean,
    is_staged boolean
);


ALTER TABLE public.applications OWNER TO bot;

--
-- Name: applications_id_seq; Type: SEQUENCE; Schema: public; Owner: bot
--

CREATE SEQUENCE public.applications_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.applications_id_seq OWNER TO bot;

--
-- Name: applications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bot
--

ALTER SEQUENCE public.applications_id_seq OWNED BY public.applications.id;


--
-- Name: attendance; Type: TABLE; Schema: public; Owner: bot
--

CREATE TABLE public.attendance (
    id integer NOT NULL,
    user_id bigint,
    nickname text,
    date date
);


ALTER TABLE public.attendance OWNER TO bot;

--
-- Name: attendance_id_seq; Type: SEQUENCE; Schema: public; Owner: bot
--

CREATE SEQUENCE public.attendance_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.attendance_id_seq OWNER TO bot;

--
-- Name: attendance_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bot
--

ALTER SEQUENCE public.attendance_id_seq OWNED BY public.attendance.id;


--
-- Name: date_joined; Type: TABLE; Schema: public; Owner: bot
--

CREATE TABLE public.date_joined (
    id integer NOT NULL,
    user_id bigint,
    nickname text,
    join_date date,
    warned_date date,
    mc_username text,
    steam_id bigint
);


ALTER TABLE public.date_joined OWNER TO bot;

--
-- Name: date_joined_id_seq; Type: SEQUENCE; Schema: public; Owner: bot
--

CREATE SEQUENCE public.date_joined_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.date_joined_id_seq OWNER TO bot;

--
-- Name: date_joined_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bot
--

ALTER SEQUENCE public.date_joined_id_seq OWNED BY public.date_joined.id;


--
-- Name: enjin; Type: TABLE; Schema: public; Owner: bot
--

CREATE TABLE public.enjin (
    id integer NOT NULL,
    session_id text,
    date_created date
);


ALTER TABLE public.enjin OWNER TO bot;

--
-- Name: enjin_id_seq; Type: SEQUENCE; Schema: public; Owner: bot
--

CREATE SEQUENCE public.enjin_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.enjin_id_seq OWNER TO bot;

--
-- Name: enjin_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bot
--

ALTER SEQUENCE public.enjin_id_seq OWNED BY public.enjin.id;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: bot
--

CREATE TABLE public.roles (
    id integer NOT NULL,
    attendance_id integer,
    role text
);


ALTER TABLE public.roles OWNER TO bot;

--
-- Name: roles_id_seq; Type: SEQUENCE; Schema: public; Owner: bot
--

CREATE SEQUENCE public.roles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.roles_id_seq OWNER TO bot;

--
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bot
--

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;


--
-- Name: application_votes id; Type: DEFAULT; Schema: public; Owner: bot
--

ALTER TABLE ONLY public.application_votes ALTER COLUMN id SET DEFAULT nextval('public.application_votes_id_seq'::regclass);


--
-- Name: applications id; Type: DEFAULT; Schema: public; Owner: bot
--

ALTER TABLE ONLY public.applications ALTER COLUMN id SET DEFAULT nextval('public.applications_id_seq'::regclass);


--
-- Name: attendance id; Type: DEFAULT; Schema: public; Owner: bot
--

ALTER TABLE ONLY public.attendance ALTER COLUMN id SET DEFAULT nextval('public.attendance_id_seq'::regclass);


--
-- Name: date_joined id; Type: DEFAULT; Schema: public; Owner: bot
--

ALTER TABLE ONLY public.date_joined ALTER COLUMN id SET DEFAULT nextval('public.date_joined_id_seq'::regclass);


--
-- Name: enjin id; Type: DEFAULT; Schema: public; Owner: bot
--

ALTER TABLE ONLY public.enjin ALTER COLUMN id SET DEFAULT nextval('public.enjin_id_seq'::regclass);


--
-- Name: roles id; Type: DEFAULT; Schema: public; Owner: bot
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- Name: application_votes application_votes_pkey; Type: CONSTRAINT; Schema: public; Owner: bot
--

ALTER TABLE ONLY public.application_votes
    ADD CONSTRAINT application_votes_pkey PRIMARY KEY (id);


--
-- Name: applications applications_pkey; Type: CONSTRAINT; Schema: public; Owner: bot
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT applications_pkey PRIMARY KEY (id);


--
-- Name: attendance attendance_pkey; Type: CONSTRAINT; Schema: public; Owner: bot
--

ALTER TABLE ONLY public.attendance
    ADD CONSTRAINT attendance_pkey PRIMARY KEY (id);


--
-- Name: date_joined date_joined_pkey; Type: CONSTRAINT; Schema: public; Owner: bot
--

ALTER TABLE ONLY public.date_joined
    ADD CONSTRAINT date_joined_pkey PRIMARY KEY (id);


--
-- Name: enjin enjin_pkey; Type: CONSTRAINT; Schema: public; Owner: bot
--

ALTER TABLE ONLY public.enjin
    ADD CONSTRAINT enjin_pkey PRIMARY KEY (id);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: bot
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: application_votes application_votes_applications_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bot
--

ALTER TABLE ONLY public.application_votes
    ADD CONSTRAINT application_votes_applications_id_fkey FOREIGN KEY (applications_id) REFERENCES public.applications(id);


--
-- Name: roles roles_attendance_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bot
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_attendance_id_fkey FOREIGN KEY (attendance_id) REFERENCES public.attendance(id);


--
-- PostgreSQL database dump complete
--

