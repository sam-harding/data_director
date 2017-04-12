import athlete
import race
import logging
import json
logging.basicConfig(filename='logs/po10populate.log',level=logging.DEBUG, format='[%(asctime)s][%(levelname)s]:%(message)s')

with open("po10_sample.json", "w") as outfile:
  a = athlete.scrape_athlete_po10(208016)
  json.dump(a, outfile, indent=2, sort_keys=True)
  logging.info("Processing Athlete {} ------ ".format(208016))
  for r in a["po10_races"]:
    print("Attempting to process (meeting_id={}, event={}, venue={}, date={})".format(r["meeting_id"], r["event"], r["venue"], r["date"]))
    parsed = race.scrape_race_po10(meeting_id=r["meeting_id"],
                        event=r["event"],
                        venue=r["venue"],
                        date=r["date"])
    json.dump(parsed, outfile, indent=2, sort_keys=True)
