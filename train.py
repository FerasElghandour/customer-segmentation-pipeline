"""Fit the population-only segmentation pipeline and export representation ratios."""
from pathlib import Path
import argparse,hashlib,json,joblib,pandas as pd
from segmentation import segment
p=argparse.ArgumentParser(description=__doc__);p.add_argument('population',type=Path);p.add_argument('customers',type=Path);p.add_argument('--clusters',type=int,default=10);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
if a.output.exists():raise ValueError('Use a new output directory')
a.output.mkdir(parents=True);pop,customers=pd.read_csv(a.population),pd.read_csv(a.customers);pipe,summary=segment(pop,customers,clusters=a.clusters);joblib.dump(pipe,a.output/'pipeline.joblib');summary.to_csv(a.output/'representation.csv',index=False)
columns=list(pop.select_dtypes(include='number').columns)
assert (pipe.predict(customers[columns])==joblib.load(a.output/'pipeline.joblib').predict(customers[columns])).all()
(a.output/'model.json').write_text(json.dumps({'seed':42,'columns':columns,'clusters':a.clusters,'population_rows':len(pop),'customer_rows':len(customers),'source_sha256':{role:hashlib.sha256(path.read_bytes()).hexdigest() for role,path in [('population',a.population),('customers',a.customers)]},'fit_scope':'Population only; customers transformed without refitting'},indent=2)+'\n')
