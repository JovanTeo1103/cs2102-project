/*******************

  Cleaning script

*******************/

-- 1. Drop dependent transaction/fact tables first
DROP TABLE IF EXISTS exits;
DROP TABLE IF EXISTS result;

-- 2. Drop intermediate tables (Stages depends on Stage Types & Locations)
DROP TABLE IF EXISTS stage;
DROP TABLE IF EXISTS rider;
DROP TABLE IF EXISTS team;
DROP TABLE IF EXISTS location;

-- 3. Drop lookup/independent tables
DROP TABLE IF EXISTS stage_type;
DROP TABLE IF EXISTS exit_reason;
DROP TABLE IF EXISTS country;