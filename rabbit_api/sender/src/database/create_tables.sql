--
-- PostgreSQL database dump
--

-- Dumped from database version 13.0
-- Dumped by pg_dump version 13.0

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
-- Name: content; Type: SCHEMA; Schema: -; Owner: postgres
--

\c postgres

CREATE SCHEMA content;


ALTER SCHEMA content OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: notifications; Type: TABLE; Schema: content; Owner: app
--

-- Создаем базовую таблицу для хранения отправленных уведомлений
CREATE TABLE IF NOT EXISTS content.notifications (
  notification_id uuid NOT NULL,
  user_id uuid NOT NULL,
  content_id varchar(250) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  type varchar(250) NOT NULL);
