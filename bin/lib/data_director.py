#Data Director class
#Acts as a manager for piping data.
#Sets up config based on a config file.
#The passes data to module as defined
import json

class DataDirector:
  
  def __init__(self):
    self.mapping = {}

  def init_config(self, file_path="config/standard_config.conf"):
    self.load_mapping(file_path)

  #Loads mapping and parses into mapping dict
  def load_mapping(self, file_path):
    with open(file_path, 'r') as f:
      self.mapping = json.load(f)