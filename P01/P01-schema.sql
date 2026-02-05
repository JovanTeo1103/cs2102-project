--
-- Group Number: 15
-- Group Members:
--   1. GOH YI HENG, RAYNER
--   2. JOVAN TEO YI
--   3. MAI KAI LER
--   4. NICHA ING SEE
--

-- 1. Regions 
CREATE TABLE IF NOT EXISTS regions (
    name TEXT PRIMARY KEY
);

-- 2. Countries
CREATE TABLE IF NOT EXISTS countries (
    ioc CHAR(3) PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    region TEXT NOT NULL REFERENCES regions(name)
);

-- 3. Locations
-- Depends on: Countries
CREATE TABLE IF NOT EXISTS locations (
    name TEXT PRIMARY KEY,
    country CHAR(3) NOT NULL REFERENCES countries(ioc)
);

-- 4. Teams
-- Depends on: Countries
CREATE TABLE IF NOT EXISTS teams (
    name TEXT PRIMARY KEY,
    country CHAR(3) NOT NULL REFERENCES countries(ioc)
);

-- 5. Riders
-- Depends on: Teams, Countries
CREATE TABLE IF NOT EXISTS riders (
    bib_number INTEGER PRIMARY KEY,
    team TEXT NOT NULL REFERENCES teams(name),
    name TEXT NOT NULL,
    dob DATE NOT NULL,
    country CHAR(3) REFERENCES countries(ioc)
);

-- 6. Stage types
CREATE TABLE IF NOT EXISTS stage_types (
    type TEXT PRIMARY KEY
);

-- 7. Stages
-- Depends on: Locations
CREATE TABLE IF NOT EXISTS stages (
    stage_number INTEGER PRIMARY KEY,
    start_location TEXT NOT NULL REFERENCES locations(name),
    finish_location TEXT NOT NULL REFERENCES locations(name),
    type TEXT NOT NULL REFERENCES stage_types(type),
    length INTEGER NOT NULL
);

-- 8. Results
-- Depends on: Stages, Riders
CREATE TABLE IF NOT EXISTS results (
    stage_number INTEGER REFERENCES stages(stage_number),
    bib_number INTEGER REFERENCES riders(bib_number),
    time_taken INTEGER,
    bonus INTEGER DEFAULT 0,
    penalty INTEGER DEFAULT 0,
    rank INTEGER,

    PRIMARY KEY (stage_number, bib_number),
    UNIQUE (stage_number, rank)
);

-- 9. Exit Reasons
-- Independent table
CREATE TABLE IF NOT EXISTS exit_reasons (
    reason TEXT PRIMARY KEY
);

-- 10. Exits
-- Depends on: Riders, Stages, Exit Reasons
CREATE TABLE IF NOT EXISTS exits (
    bib_number INTEGER PRIMARY KEY REFERENCES riders(bib_number),
    stage_number INTEGER NOT NULL REFERENCES stages(stage_number),
    reason TEXT NOT NULL REFERENCES exit_reasons(reason)
);
