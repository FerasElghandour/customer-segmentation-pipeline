"""Offline example using the public implementation; see README for evidence scope."""
import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))
os.chdir(ROOT)

import numpy as np
import pandas as pd
from segmentation import segment
# Generated fixtures demonstrate current API behavior only.
rng=np.random.default_rng(5)
population=pd.DataFrame(np.vstack([rng.normal(-4,.1,(20,3)),rng.normal(4,.1,(20,3))]),columns=['a','b','c'])
customers=population.iloc[20:].copy()
pipe,result=segment(population,customers,clusters=2)
import json
print(json.dumps(result.to_dict(orient="records"), indent=2))
