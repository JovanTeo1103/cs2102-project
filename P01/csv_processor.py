import csv

"""
Simple I/O Library
  We assume all files are in UTF-8
"""
# Text
def read_text(file):
  """
  Read a file as text.  The name of the file is
  given as `file`.  The file is treated as utf-8
  format.

  The return type is a String.
  """
  with open(file, encoding='utf-8') as f:
    return f.read()
  return ''
def write_text(file, data):
  """
  Write the data into a file as text.  The name
  of the file is given as `file`.  The data is
  given as `data`.  The file is treated as utf-8
  format.

  There is no return value.
  """
  with open(file, 'w', encoding='utf-8') as f:
    f.write(data)

# CSV
def read_csv(file):
  """
  Read a file as comma-separated value (csv).
  The name of the file is given as `file`.  The
  file is treated as utf-8 format.

  The return type is a list-of-list.
  """
  res = []
  with open(file, encoding='utf-8') as f:
    rd = csv.reader(f)
    for row in rd:
      res.append(row)
  return res
def write_csv(file, data):
  """
  Write the data into a file as a comma-separated
  value (csv).  The name of the file is given as
  `file`.  The data is given as `data`.  The file
  is treated as utf-8 format.  The data is treated
  as a list-of-list.

  There is no return value.
  """
  with open(file, 'w', encoding='utf-8') as f:
    wt = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in data:
      wt.writerow(row)




"""
Helper functions
"""
def as_str(v):
  """
  Return the value as a string that can be
  accepted by postgresql as string.
  """
  if not v or v == '':  # Handle empty strings as NULL
    return 'NULL'
  s = f'{v}'.replace("'", "''")
  return f"'{s}'"
def as_int(v):
  """
  Return the value as a string that can be
  accepted by postgresql as integer.
  """
  return f'{v}'




"""
EXAMPLE
  Study the following example on how to process
  the csv file and write a file containing the
  INSERT statements.
"""
def process(file, out):
  # reading the data (skip header row)
  data = read_csv(file)[1:]

  # the expected output
  line = ''

  # Track unique entities to avoid duplicates
  countries_seen = set()
  teams_seen = set()
  riders_seen = set()
  locations_seen = set()
  
  # Collect all Stage 1 rows first
  stage1_data = []
  for row in data:
    if row[1] == '1':  # stage column is index 1
      stage1_data.append(row)
  
  # Insert Countries first
  line += '-- Insert Countries\n'
  for row in stage1_data:
    # Start country
    start_code = row[8]
    start_name = row[9]
    start_region = row[10]
    if start_code not in countries_seen:
      line += f'INSERT INTO countries (ioc, name, region) VALUES ({as_str(start_code)}, {as_str(start_name)}, {as_str(start_region)});\n'
      countries_seen.add(start_code)
    
    # Finish country
    finish_code = row[12]
    finish_name = row[13]
    finish_region = row[14]
    if finish_code not in countries_seen:
      line += f'INSERT INTO countries (ioc, name, region) VALUES ({as_str(finish_code)}, {as_str(finish_name)}, {as_str(finish_region)});\n'
      countries_seen.add(finish_code)
    
    # Rider country (if exists)
    rider_code = row[20]
    rider_country_name = row[21]
    rider_region = row[22]
    if rider_code and rider_code not in countries_seen:
      line += f'INSERT INTO countries (ioc, name, region) VALUES ({as_str(rider_code)}, {as_str(rider_country_name)}, {as_str(rider_region)});\n'
      countries_seen.add(rider_code)
    
    # Team country
    team_code = row[23]
    team_country_name = row[24]
    team_region = row[25]
    if team_code not in countries_seen:
      line += f'INSERT INTO countries (ioc, name, region) VALUES ({as_str(team_code)}, {as_str(team_country_name)}, {as_str(team_region)});\n'
      countries_seen.add(team_code)
  
  # Insert Locations
  line += '\n-- Insert Locations\n'
  for row in stage1_data:
    start_loc = row[7]
    start_code = row[8]
    finish_loc = row[11]
    finish_code = row[12]
    
    if start_loc not in locations_seen:
      line += f'INSERT INTO locations (name, country) VALUES ({as_str(start_loc)}, {as_str(start_code)});\n'
      locations_seen.add(start_loc)
    
    if finish_loc not in locations_seen:
      line += f'INSERT INTO locations (name, country) VALUES ({as_str(finish_loc)}, {as_str(finish_code)});\n'
      locations_seen.add(finish_loc)
  
  # Insert Teams
  line += '\n-- Insert Teams\n'
  for row in stage1_data:
    team = row[18]
    team_country = row[23]
    if team not in teams_seen:
      line += f'INSERT INTO teams (name, country) VALUES ({as_str(team)}, {as_str(team_country)});\n'
      teams_seen.add(team)
  
  # Insert Riders
  line += '\n-- Insert Riders\n'
  for row in stage1_data:
    bib = row[2]
    rider_name = row[17]
    dob = row[19]
    team = row[18]
    rider_country = row[20]
    
    if bib not in riders_seen:
      line += f'INSERT INTO riders (bib_number, team, name, dob, country) VALUES ({as_int(bib)}, {as_str(team)}, {as_str(rider_name)}, {as_str(dob)}, {as_str(rider_country)});\n'
      riders_seen.add(bib)
  
  # Insert Stage
  line += '\n-- Insert Stage 1\n'
  if stage1_data:
    row = stage1_data[0]  # Just need one row for stage info
    stage_num = row[1]
    start_loc = row[7]
    finish_loc = row[11]
    length = row[15]
    stage_type = row[16]
    line += f'INSERT INTO stages (stage_number, start_location, finish_location, type, length) VALUES ({as_int(stage_num)}, {as_str(start_loc)}, {as_str(finish_loc)}, {as_str(stage_type)}, {as_int(length)});\n'
  
  # Insert Results
  line += '\n-- Insert Results for Stage 1\n'
  for row in stage1_data:
    bib = row[2]
    stage_num = row[1]
    rank = row[3]
    time = row[4]
    bonus = row[5]
    penalty = row[6]
    line += f'INSERT INTO results (stage_number, bib_number, time_taken, bonus, penalty, rank) VALUES ({as_int(stage_num)}, {as_int(bib)}, {as_int(time)}, {as_int(bonus)}, {as_int(penalty)}, {as_int(rank)});\n'

  # write into a file
  write_text(out, line)


# Change the input filename and/or the output filename
process('tdF-2025.csv', 'P01-data.sql')