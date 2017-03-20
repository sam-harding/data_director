#This file includes functions for returning an object based off
#data from an athletes profile on Power of 10
from bs4 import BeautifulSoup
import urllib

def scrape_athlete_po10(po10_athlete_id):
  output = {}
  #Required keys
  output["po10_athlete_id"] = None
  output["name"] = None
  output["po10_athlete_id"] = po10_athlete_id
 
  # Initialize URL and BeautifulSoup
  url = "http://www.powerof10.info/athletes/profile.aspx?athleteid={}".format(po10_athlete_id)
  r = urllib.urlopen(url).read()
  soup = BeautifulSoup(r, "html.parser")

  # Check profile exists
  errors = soup.find_all("span", {"id":"cphBody_lblErrorMessage"})
  if len(errors[0].text) > 0:
    return False

  #Get athlete name
  ath_name = soup.find_all("tr", class_="athleteprofilesubheader")
  ath_name = ath_name[0].find_all("td")
  ath_name = ath_name[0].find_all("h2")
  output["name"] = ath_name[0].get_text().lstrip()

  #Get athlete information 
  ath_info = soup.find_all("div", id="cphBody_pnlAthleteDetails")
  ath_info = ath_info[0].find_all("table", cellpadding="2")
  for element_i in ath_info:
    ath_info_block = element_i.find_all("tr")
    for element_j in ath_info_block:
      split = element_j.get_text().split(":", 1)
      output[split[0]] = split[1]

  return output

