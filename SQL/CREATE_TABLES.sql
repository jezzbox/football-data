create table country (
    country_id SERIAL,
    country_name VARCHAR(200),
    CONSTRAINT country_pkey PRIMARY KEY(country_id)
);

create table city (
    city_id SERIAL,
    city_name VARCHAR(200),
    country_id INT,
    CONSTRAINT city_pkey PRIMARY KEY(city_id),
    CONSTRAINT country_fkey FOREIGN KEY(country_id) REFERENCES country(country_id)
);
create table league (
    league_id SERIAL,
    league_name VARCHAR(200),
    region VARCHAR(200),
    league_format VARCHAR(200),
    CONSTRAINT league_pkey PRIMARY KEY(league_id)
);

create table country_eligibility (
    eligibility_id SERIAL,
    country_id INT,
    league_id INT,
    eligible_from DATE,
    eligible_to DATE,
    CONSTRAINT eligibility_pkey PRIMARY KEY(eligibility_id),
    CONSTRAINT league_fkey FOREIGN KEY(league_id) references league(league_id),
    CONSTRAINT country_fkey FOREIGN KEY(country_id) references country(country_id),
    CONSTRAINT uq_eligibility_key UNIQUE(country_id,league_id,eligible_from, eligible_to)
);

create table stadium (
    stadium_id SERIAL,
    stadium_name VARCHAR(300),
    city_id int,
    CONSTRAINT stadium_pkey PRIMARY KEY(stadium_id),
    CONSTRAINT city_fkey FOREIGN KEY(city_id) REFERENCES city(city_id)
);

create table season (
    season_id SERIAL,
    league_id INT,
    season_start DATE,
    season_end DATE,
    CONSTRAINT season_pkey PRIMARY KEY(season_id),
    CONSTRAINT league_fkey FOREIGN KEY(league_id) REFERENCES league(league_id),
    CONSTRAINT uq_season_key UNIQUE(season_id,league_id,season_start)
);

create table team (
    team_id SERIAL,
    official_team_name VARCHAR(200),
    team_nickname VARCHAR(2000),
    city_id INT,
    CONSTRAINT team_pkey PRIMARY KEY(team_id),
    CONSTRAINT country_fkey FOREIGN KEY(city_id) REFERENCES city(city_id)
);

create table match (
    match_id SERIAL,
    season_id INT,
    match_number INT,
    match_date DATE,
    kick_off TIME,
    stadium_id INT,
    home_team_id INT,
    away_team_id INT,
    CONSTRAINT match_pkey PRIMARY KEY(match_id),
    CONSTRAINT stadium_fkey FOREIGN KEY(stadium_id) REFERENCES stadium(stadium_id),
    CONSTRAINT home_team_fkey FOREIGN KEY(home_team_id) REFERENCES team(team_id),
    CONSTRAINT away_team_fkey FOREIGN KEY(away_team_id) REFERENCES team(team_id),
    CONSTRAINT season_fkey FOREIGN KEY(season_id) REFERENCES season(season_id),
    CONSTRAINT uq_match_key UNIQUE(season_id,match_number,home_team_id,away_team_id)
);

create table person (
    person_id SERIAL,
    first_name varchar(200),
    surname varchar(200),
    other_names varchar(200),
    city_id int,
    date_of_birth DATE,
    role VARCHAR(200),
    height DECIMAL,
    nationality VARCHAR(10),
    football_position varchar(10),
    CONSTRAINT person_pkey PRIMARY KEY(member_id),
    CONSTRAINT city_fkey FOREIGN KEY(city_id) REFERENCES city(city_id),
    CONSTRAINT uq_person_key UNIQUE (first_name,surname,other_names,date_of_birth,nationality)
);
create table match_attendance (
    attendance_id SERIAL,
    person_id int,
    position VARCHAR(200),
    team_id int,
    match_id int,
    match_half int,
    time_sent_on DATE,
    time_sent_off DATE,
    CONSTRAINT attendance_pkey PRIMARY KEY(attendance_id),
    CONSTRAINT person_fkey FOREIGN KEY(person_id) REFERENCES person(person_id),
    CONSTRAINT team_fkey FOREIGN KEY(team_id) REFERENCES team(team_id),
    CONSTRAINT match_fkey FOREIGN KEY(match_id) REFERENCES match(match_id),
    CONSTRAINT unique_attendance_key UNIQUE(member_id,match_id, match_half)

);
create table match_activity (
    activity_id SERIAL,
    attendance_id int,
    activity_type VARCHAR(200),
    activity_time TIME,
    disallowed BOOLEAN,
    CONSTRAINT activity_pkey PRIMARY KEY(activity_id),
    CONSTRAINT attendance_fkey FOREIGN KEY(attendance_id) REFERENCES match_attendance(attendance_id)
);

CREATE TABLE contract
(
    contract_id    SERIAL,
    person_id      INT,
    team_id        INT,
    cost           MONEY,
    clause         VARCHAR(200),
    contract_type  VARCHAR(200),
    contract_start DATE,
    contract_end   DATE,
    actual_contract_end     DATE,
    CONSTRAINT contract_pkey PRIMARY KEY (contract_id),
    CONSTRAINT member_fkey FOREIGN KEY (member_id) REFERENCES team_member (member_id),
    CONSTRAINT team_fkey FOREIGN KEY (team_id) REFERENCES team (team_id),
    CONSTRAINT unique_contract_key UNIQUE (person_id, team_id, contract_start, contract_type)
);

create table home_stadium
(
    home_stadium_id   SERIAL,
    team_id           INT,
    stadium_id        INT,
    home_stadium_from DATE,
    home_stadium_to   DATE,
    CONSTRAINT home_stadium_pkey PRIMARY KEY (home_stadium_id),
    CONSTRAINT team_fkey FOREIGN KEY (team_id) REFERENCES team(team_id)
    CONSTRAINT uq_home_stadium UNIQUE (team_id, stadium_id, home_stadium_from, home_stadium_to)
);