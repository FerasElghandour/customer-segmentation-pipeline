import numpy as np
import pandas as pd
from segmentation import segment
rng=np.random.default_rng(5)
population=pd.DataFrame(np.vstack([rng.normal(-4,.1,(20,3)),rng.normal(4,.1,(20,3))]),columns=['a','b','c'])
customers=population.iloc[20:].copy()
pipe,result=segment(population,customers,clusters=2)
assert abs(result['population_share'].sum()-1)<1e-9 and abs(result['customer_share'].sum()-1)<1e-9
assert sorted(result['representation_ratio'].tolist())==[0.,2.]
assert np.allclose(pipe.named_steps['scale'].mean_,population.mean())
print('Population-fitted preprocessing, aligned customer projection, and representation ratios passed.')
