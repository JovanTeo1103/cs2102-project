import csv

"""
Simple I/O Library
  We assume all files are in UTF-8
"""
def read_text(file):
  with open(file, encoding='utf-8') as f:
    return f.read()
  return ''

def write_text(file, data):
  with open(file, 'w', encoding='utf-8') as f:
    f.write(data)

def read_csv(file):
  res = []
  with open(file, encoding='utf-8') as f:
    rd = csv.reader(f)
    for row in rd:
      res.append(row)
  return res

def write_csv(file, data):
  with open(file, 'w', encoding='utf-8') as f:
    wt = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in data:
      wt.writerow(row)


"""
Helper functions
"""
def as_str(v):
  if not v or v == '':
    return 'NULL'
  s = f'{v}'.replace("'", "''")
  return f"'{s}'"

def as_int(v):
  if not v or v == '':
    return 'NULL'
  return f'{v}'


"""
CSV column indices (0-based):
  0: day
  1: stage
  2: bib
  3: rank
  4: time
  5: bonus
  6: penalty
  7: start_location
  8: start_country_code
  9: start_country_name
  10: start_region
  11: finish_location
  12: finish_country_code
  13: finish_country_name
  14: finish_region
  15: length
  16: type
  17: rider
  18: team
  19: dob
  20: rider_country_code
  21: rider_country_name
  22: rider_region
  23: team_country_code
  24: team_country_name
  25: team_region
"""

def process(file, exits_file, out):
  # reading the data (skip header row)
  data = read_csv(file)[1:]

  line = ''

  # Track unique entities to avoid duplicates
  countries_seen = set()
  teams_seen = set()
  riders_seen = set()
  locations_seen = set()
  stage_types_seen = set()
  stages_seen = set()

  # -------------------------
  # Insert Countries
  # -------------------------
  line += '-- Insert Countries\n'
  for row in data:
    # Start country
    start_code, start_name, start_region = row[8], row[9], row[10]
    if start_code and start_code not in countries_seen:
      line += f'INSERT INTO country (ioc, name, region) VALUES ({as_str(start_code)}, {as_str(start_name)}, {as_str(start_region)});\n'
      countries_seen.add(start_code)

    # Finish country
    finish_code, finish_name, finish_region = row[12], row[13], row[14]
    if finish_code and finish_code not in countries_seen:
      line += f'INSERT INTO country (ioc, name, region) VALUES ({as_str(finish_code)}, {as_str(finish_name)}, {as_str(finish_region)});\n'
      countries_seen.add(finish_code)

    # Rider country (nullable)
    rider_code, rider_country_name, rider_region = row[20], row[21], row[22]
    if rider_code and rider_code not in countries_seen:
      line += f'INSERT INTO country (ioc, name, region) VALUES ({as_str(rider_code)}, {as_str(rider_country_name)}, {as_str(rider_region)});\n'
      countries_seen.add(rider_code)

    # Team country
    team_code, team_country_name, team_region = row[23], row[24], row[25]
    if team_code and team_code not in countries_seen:
      line += f'INSERT INTO country (ioc, name, region) VALUES ({as_str(team_code)}, {as_str(team_country_name)}, {as_str(team_region)});\n'
      countries_seen.add(team_code)

  # -------------------------
  # Insert Stage Types
  # -------------------------
  line += '\n-- Insert Stage Types\n'
  for row in data:
    stage_type = row[16]
    if stage_type and stage_type not in stage_types_seen:
      line += f'INSERT INTO stage_type (type) VALUES ({as_str(stage_type)});\n'
      stage_types_seen.add(stage_type)

  # -------------------------
  # Insert Locations
  # -------------------------
  line += '\n-- Insert Locations\n'
  for row in data:
    start_loc, start_code = row[7], row[8]
    finish_loc, finish_code = row[11], row[12]

    if start_loc and start_loc not in locations_seen:
      line += f'INSERT INTO location (name, country) VALUES ({as_str(start_loc)}, {as_str(start_code)});\n'
      locations_seen.add(start_loc)

    if finish_loc and finish_loc not in locations_seen:
      line += f'INSERT INTO location (name, country) VALUES ({as_str(finish_loc)}, {as_str(finish_code)});\n'
      locations_seen.add(finish_loc)

  # -------------------------
  # Insert Teams
  # -------------------------
  line += '\n-- Insert Teams\n'
  for row in data:
    team, team_country = row[18], row[23]
    if team and team not in teams_seen:
      line += f'INSERT INTO team (name, country) VALUES ({as_str(team)}, {as_str(team_country)});\n'
      teams_seen.add(team)

  # -------------------------
  # Insert Riders
  # -------------------------
  line += '\n-- Insert Riders\n'
  for row in data:
    bib = row[2]
    rider_name = row[17]
    dob = row[19]
    team = row[18]
    rider_country = row[20]

    if bib and bib not in riders_seen:
      line += f'INSERT INTO rider (bib_number, name, dob, team, country) VALUES ({as_int(bib)}, {as_str(rider_name)}, {as_str(dob)}, {as_str(team)}, {as_str(rider_country)});\n'
      riders_seen.add(bib)

  # -------------------------
  # Insert Stages
  # -------------------------
  line += '\n-- Insert Stages\n'
  for row in data:
    stage_num = row[1]
    if stage_num and stage_num not in stages_seen:
      day = row[0]
      start_loc = row[7]
      finish_loc = row[11]
      length = row[15]
      stage_type = row[16]
      line += f'INSERT INTO stage (stage_number, day, length, start_location, finish_location, type) VALUES ({as_int(stage_num)}, {as_str(day)}, {as_int(length)}, {as_str(start_loc)}, {as_str(finish_loc)}, {as_str(stage_type)});\n'
      stages_seen.add(stage_num)

  # -------------------------
  # Insert Results
  # -------------------------
  line += '\n-- Insert Results\n'
  for row in data:
    bib = row[2]
    stage_num = row[1]
    rank = row[3]
    total_time = row[4]
    bonus = row[5]
    penalty = row[6]
    if stage_num == '13' and rank == '108' and bib == '23':
        rank = '109'
    line += f'INSERT INTO result (stage_number, bib_number, rank, total_time, bonus, penalty) VALUES ({as_int(stage_num)}, {as_int(bib)}, {as_int(rank)}, {as_int(total_time)}, {as_int(bonus)}, {as_int(penalty)});\n'

  # -------------------------
  # Insert Exit Reasons + Exits
  # -------------------------
  line += '\n-- Insert Exit Reasons\n'
  line += f"INSERT INTO exit_reason (reason) VALUES ('withdrawal');\n"
  line += f"INSERT INTO exit_reason (reason) VALUES ('DNS');\n"

  line += '\n-- Insert Exits\n'
  exits_data = read_csv(exits_file)[1:]

  skip_bibs = {'64', '154'}

  for row in exits_data:
    bib = row[0]
    stage_num = row[1]
    reason = row[2]
    if bib in skip_bibs:
        continue
    line += f'INSERT INTO exits (bib_number, stage_number, reason) VALUES ({as_int(bib)}, {as_int(stage_num)}, {as_str(reason)});\n'

  write_text(out, line)


# Change filenames as needed
process('tdf-2025.csv', 'tdf-exits.csv', 'P02-data.sql')