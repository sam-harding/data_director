#A method of running Data Director
#Data gets piped in via standard input.
from lib.data_director import *

data_director = DataDirector()
data_director.init_config()