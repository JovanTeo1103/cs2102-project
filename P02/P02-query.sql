--
-- Group Number: 15
-- Group Members:
--   1. GOH YI HENG, RAYNER
--   2. JOVAN TEO YI
--   3. MAI KAI LER
--   4. NICHA ING SEE
--

-- entities
CREATE TABLE IF NOT EXISTS country (
    ioc CHAR(3) PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    region TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS team (
    name TEXT PRIMARY KEY,
    country CHAR(3) NOT NULL REFERENCES country(ioc)
);

CREATE TABLE IF NOT EXISTS rider (
    bib_number INTEGER PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    dob DATE NOT NULL,
    team TEXT NOT NULL REFERENCES team(name),
    country CHAR(3) REFERENCES country(ioc)
);

CREATE TABLE IF NOT EXISTS stage_type (
    type TEXT PRIMARY KEY CHECK (type IN ('hilly', 'flat', 'mountain', 
    'individual time-trial', 'team time-trial'))
);

CREATE TABLE IF NOT EXISTS location (
    name TEXT PRIMARY KEY,
    country CHAR(3) NOT NULL REFERENCES country(ioc)
);

CREATE TABLE IF NOT EXISTS stage (
    stage_number INTEGER PRIMARY KEY,
    day DATE NOT NULL,
    length INTEGER NOT NULL CHECK (length > 0),
    start_location TEXT NOT NULL REFERENCES location(name),
    finish_location TEXT NOT NULL REFERENCES location(name),
    type TEXT NOT NULL REFERENCES stage_type(type)

);

-- relationships
CREATE TABLE IF NOT EXISTS result (
    stage_number INTEGER REFERENCES stage(stage_number),
    bib_number INTEGER REFERENCES rider(bib_number),
    bonus INTEGER NOT NULL CHECK (bonus >= 0),
    penalty INTEGER NOT NULL CHECK (penalty >= 0),
    rank INTEGER NOT NULL CHECK (rank > 0),
    total_time INTEGER NOT NULL CHECK (total_time >= 0),

    PRIMARY KEY (stage_number, bib_number),
    UNIQUE (stage_number, rank)
);

CREATE TABLE IF NOT EXISTS exit_reason (
    reason TEXT PRIMARY KEY CHECK (reason IN ('withdrawal', 'DNS'))
);

CREATE TABLE IF NOT EXISTS exits (
    bib_number   INTEGER PRIMARY KEY REFERENCES rider(bib_number),
    stage_number INTEGER NOT NULL    REFERENCES stage(stage_number),
    reason       TEXT    NOT NULL    REFERENCES exit_reason(reason)
);