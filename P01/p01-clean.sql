/*******************

  Cleaning script

*******************/

-- 1. Drop dependent transaction/fact tables first
DROP TABLE IF EXISTS exits;
DROP TABLE IF EXISTS results;

-- 2. Drop intermediate tables (Stages depends on Stage Types & Locations)
DROP TABLE IF EXISTS stages;
DROP TABLE IF EXISTS riders;
DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS locations;

-- 3. Drop lookup/independent tables
DROP TABLE IF EXISTS stage_types;
DROP TABLE IF EXISTS exit_reasons;
DROP TABLE IF EXISTS countries;
DROP TABLE IF EXISTS regions;