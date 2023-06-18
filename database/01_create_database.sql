CREATE DATABASE gestor_de_usuarios;

\c gestor_de_usuarios

CREATE SCHEMA IF NOT EXISTS "public";

CREATE TYPE "public"."acess" AS ENUM ('admin', 'basic', 'manager');

CREATE TABLE "public"."user" (
    matricula      VARCHAR(250)         NOT NULL,
    name    VARCHAR(250)    NOT NULL,
    endereco    VARCHAR(250)    NOT NULL,
    rg    VARCHAR(100),
    password    TEXT    NOT NULL,
    active    BOOLEAN         NOT NULL DEFAULT TRUE,
    updated_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    acess  "public"."acess"    NOT NULL DEFAULT 'basic',

    CONSTRAINT "PK_matricula" PRIMARY KEY ( "matricula" )   
);

CREATE TABLE "public"."disciplina" (
    codigo VARCHAR(8) NOT NULL,
    nome VARCHAR(250) NOT NULL,
    horario VARCHAR(1) NOT NULL,
    turma INTEGER NOT NULL,

    CONSTRAINT "PK_codigo" PRIMARY KEY ( "codigo" )
);