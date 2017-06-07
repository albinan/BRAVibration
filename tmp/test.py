import sys
sys.path.append('C:/Users/ReVibe/Documents/Albin/MasterSnake/LIB')
from oscilloscope import Oscilloscope

scope = Oscilloscope(activeChannels=[1], memdepth=12000)

print(scope.get_memdepth())
