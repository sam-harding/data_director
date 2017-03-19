#This file includes functions for returning an object based off
#data from an athletes profile on Power of 10
from bs4 import BeautifulSoup
import urllib

def scrape_athlete_po10(po10_athlete_id):
  output = {}
  #Required keys
  output["po10_athlete_id"] = None
  output["name_first"] = None
  output["name_last"] = None
 
  # Initialize URL and BeautifulSoup
  url = "http://www.powerof10.info/athletes/profile.aspx?athleteid={}".format(po10_athlete_id)
  r = urllib.urlopen(url).read()
  soup = BeautifulSoup(r, "html.parser")

  # Check profile exists
  errors = soup.find_all("span", {"id":"cphBody_lblErrorMessage"})
  if len(errors[0].text) > 0:
    return False

  return output

