import numpy as np
import pandas as pd

a = np.array([1,2,17,20,16,3,5,4])
aPandas = pd.Series(a)
aPandas.plot()
aPandas[aPandas > 15].plot(color = 'red')