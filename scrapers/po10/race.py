#This file includes functions for returning an object based off
#data from a race on Power of 10
from bs4 import BeautifulSoup
import urllib
import datetime
import calendar
import uuid

def scrape_race_po10(meeting_id=None, event=None, venue=None, date=None):
  month_list = dict(Jan=1, Feb=2, Mar=3, Apr=4, May=5, Jun=6, Jul=7, Aug=8, Sep=9, Oct=10, Nov=11, Dec=12)
  if meeting_id == None:
    return False

  overall_output = {"races":[], "performances":[]} #List of races and perfs



  # Initialize URL and BeautifulSoup
  url = "http://www.thepowerof10.info/results/results.aspx?meetingid={}".format(meeting_id)

  if event != None:
    url += "&event={}".format(event)
  if venue != None:
    url += "&venue={}".format(venue)
  if date != None:
    url += "&date={}".format(date)

  r = urllib.urlopen(url).read()
  print("Processing {}".format(url))
  soup = BeautifulSoup(r, "html.parser")

  #Check race exists
  #TODO

  #Get event details
  event_detail = soup.find_all("div", id="pnlMainGeneral")
  event_detail = event_detail[0].find_all("span", id="cphBody_lblMeetingDetails")
  event_name = event_detail[0].find_all("b")[0].getText()
  event_link = event_detail[0].find_all("a", href=True)[0]["href"]
  event_location = event_detail[0].find_all("br")[0].contents[0]
  event_date = event_detail[0].find_all("br")[0].contents[1].stripped_strings.next().strip().split(" ")
  event_day = event_date[0]
  event_month = event_date[1]
  event_year = event_date[2]
  if int(event_year) < 30:
    event_year = "20{}".format(event_year)
  else:
    event_year = "19{}".format(event_year)

  #Cycle through individual races
  multi_race_block = soup.find_all("table", id="cphBody_dgP")
  block_iter = multi_race_block[0].find_all("tr")

  uuid_link = None

  for section in block_iter:

    #This section handles individual race information
    if section.get("style") == "background-color:DarkGray;":
      if "race" in locals():
        overall_output["races"].append(race)

      # Start of new race
      race = {}
      race["po10_event_id"] = meeting_id
      race["event_name"] = event_name
      race["event_link"] = event_link
      race["event_location"] = event_location
      uuid_link = uuid.uuid1().int
      race["uuid_link"] = uuid_link

      race_array = section.getText().strip().split(" ")
      race["event"] = race_array[0]
      race["event_age_group"] = race_array[1]
      if len(race_array) == 3:
        race["event_round"] = race_array[2]
        day = event_day
        month = event_month
      if len(race_array) == 4:
        # Lacks event_round
        race["event_round"] = "F"
        day = race_array[2].lstrip("(")
        month = race_array[3].rstrip(")")
      elif len(race_array) == 5:
        # Includes event_round
        race["event_round"] = race_array[2]
        day = race_array[3].lstrip("(")
        month = race_array[4].rstrip(")")

      #turn date_of_race into timestamp
      date_of_race = datetime.date(int(event_year), month_list[month], int(day))
      timestamp = calendar.timegm(date_of_race.timetuple())

      race["event_timestamp"] = timestamp


      # Tidy up last race if required
      if race != None:
        overall_output["races"].append(race)

    #This section pulls performances
    if section.get("style") == "background-color:WhiteSmoke;" or section.get("style") == "background-color:Gainsboro;":
      perf = {}
      for idx, item in enumerate(section):
        #Shift IDX if there is an additional field (such as indoor)
        idx_shifter = 0
        idx = idx + idx_shifter

        print("idx={} item={}".format(idx, item))
        # 1 = Position
        if idx == 1:
          perf["position"] = item.getText()

        # 2 = Performance
        if idx == 2:
          perf["performance"] = item.getText()

        # 3 = Athlete Name
        if idx == 3:
          try:
            perf["athlete_id_po10"] = item.a["href"].split("=")[1]
          except TypeError:
            perf["is_indoors"] = True
            idx_shifter -= 1

        # 4 = PB or SB
        if idx == 4:
          perf["was_pb"] = False
          perf["was_sb"] = False
          if item.getText() == "PB":
            perf["was_pb"] = True
            perf["was_sb"] = True
          elif item.getText() == "SB":
            perf["was_sb"] = True
        
        # 5 = Age Group
        if idx == 5:
          perf["age_group"] = item.getText()

        # 6 = Gender
        if idx == 6:
          perf["gender"] = item.getText()

        # 7 = Year in age group
        if idx == 7:
          perf["age_group_year"] = item.getText()

        # 8 = Coach
        if idx == 8 and item.a != None:
          perf["coach_id_po10"] = item.a["href"].split("=")[1]

        # 9 = Club
        if idx == 9:
          perf["club_name"] = item.getText()

      # Link to Race
      perf["uuid_link"] = uuid_link

      overall_output["performances"].append(perf)


  return overall_output