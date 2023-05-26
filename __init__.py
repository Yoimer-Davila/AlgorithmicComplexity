import sys
folder_source = './AlgorithmicComplexity'
if folder_source not in sys.path:
    sys.path.append(folder_source)


from .graphs import *
from .utilities import *

"""
If you get error in Google Collab import run the bellow code at the beginning
import sys
sys.path.append('./AlgorithmicComplexity')
"""