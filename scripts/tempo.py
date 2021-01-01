import numpy as np
import scipy.interpolate
from .sheets import tempo as temposheet

times = np.array(temposheet.times)
measures = np.array(temposheet.beats)/4
t2m = scipy.interpolate.interp1d(times,measures,fill_value='extrapolate')
m2t = scipy.interpolate.interp1d(measures,times,fill_value='extrapolate')