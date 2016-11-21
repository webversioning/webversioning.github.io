import difflib
import json
import datetime
import time
import os
import requests
from pprint import pprint
from pyquery import PyQuery as pq

def get_data():
  with open('data/load_data/data.json') as fp:
    try:
      data = json.load(fp)
    except ValueError:
      data = []

  return data


def read_file(file_path):
  with open(file_path) as fp:
    data = fp.read()
  return data


def write_file(domain, url, data, add_timestamp=True):
  time = "*" + str(datetime.datetime.now())
  filename = url + time
  dir_path = 'data/store_data/' + domain + "/" + url + "/" + filename
  with open(dir_path, 'w') as fp:
    fp.write(data)
  return


def get_last_file(domain, url):
  dir_path = 'data/store_data/' + domain + "/" + url
  if not os.path.exists(dir_path):
    os.makedirs(dir_path)
  all_files = os.listdir(dir_path)
  if not all_files:
    return ''

  last_file = all_files[0]
  last_time = os.stat(dir_path + "/" + last_file)

  for f in all_files:
    new_time = os.stat(dir_path + "/" + f).st_mtime
    if new_time > last_time:
      last_time = new_time
      last_file = f
  return read_file(dir_path + "/" + last_file)


def get_new_file(url):
  r = requests.get(url)
  if r.status_code != 200:
    raise ValueError("Couldn't GET %s" % url)
  return r.text.strip()


def perform_diff(last_file, new_file):

  if not last_file and not new_file:
    return [], False

  last_file_lines = last_file.splitlines()
  new_file_lines = new_file.splitlines()

  diff = []
  is_diff = False
  for line in difflib.ndiff(last_file_lines, new_file_lines):
    start = line[0:2].strip()
    if is_diff or start == '+' or start == '-' or start == '?':
      is_diff = True
    if start != '?':
      diff.append(line)
  return diff, is_diff


def notify():
  pass


def perform_diff_and_act(domain, url, last_file, new_file, divs = []):
  if divs:
      last_selector = pq(last_file)
      new_selector = pq(new_file)
      for div in divs:
          if div['is_id']:
            query = "#" + div['name']
          else:
            query = "." + div['name']
          diff, is_diff = perform_diff(str(last_selector(query)), str(new_selector(query)))
          if is_diff:
            print "CHANGES DETECTED IN DIVS"
            notify()
          else:
            print "NO CHANGES DETECTED"
            
  diff, is_diff = perform_diff(last_file, new_file)
  if is_diff:
    write_file(domain, clean(url), new_file)
    print "CHANGES DETECTED"
  else:
    # TODO: log that no changes were found
    print "NO CHANGES DETECTED"
    pass


def analyse(domain, page_data):
  print 'ANALYSING', domain, page_data
  url = page_data['url']
  divs = page_data.get('divs', [])
  last_file = get_last_file(domain, clean(url))
  new_file = get_new_file(url)
  perform_diff_and_act(domain, url, last_file, new_file, divs)


def clean(inp):
  inp = inp.replace('http://', '')
  inp = inp.replace('https://', '')
  inp = inp.replace('www.', '')
  return inp


def run():
  data = get_data()

  # TODO: the analyse function should be called repeatedly
  # at certain intervals

  for domain_dict in data:
    domain = domain_dict.keys()[0]
    domain = clean(domain)
    pages = domain_dict[domain]['pages']
    for page in pages:
      analyse(domain, page)