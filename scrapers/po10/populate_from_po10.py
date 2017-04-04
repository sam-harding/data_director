import athlete
import race
import logging
logging.basicConfig(filename='logs/po10populate.log',level=logging.DEBUG, format='[%(asctime)s][%(levelname)s]:%(message)s')

a = athlete.scrape_athlete_po10(208016)
logging.info("Processing Athlete {} ------ ".format(208016))
for r in a["po10_races"]:
  print("Attempting to process (meeting_id={}, event={}, venue={}, date={})".format(r["meeting_id"], r["event"], r["venue"], r["date"]))
  print(race.scrape_race_po10(meeting_id=r["meeting_id"],
                        event=r["event"],
                        venue=r["venue"],
                        date=r["date"]))