"""Population-fitted segmentation and customer representation ratios."""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

def segment(population,customers,clusters=10,components=.9,seed=42):
    if not isinstance(clusters,int) or clusters<2 or len(population)<clusters:raise ValueError('Need enough population rows for at least two clusters')
    columns=list(population.select_dtypes(include='number').columns)
    if not columns or set(columns)-set(customers):raise ValueError('Shared numeric feature columns required')
    a,b=population[columns].copy(),customers[columns].copy()
    if len(b)==0 or a.isna().all().any():raise ValueError('Empty customers or entirely missing population feature')
    if np.isinf(a.to_numpy()).any() or np.isinf(b.to_numpy()).any():raise ValueError('Infinite features are invalid')
    pipe=Pipeline([('impute',SimpleImputer(strategy='median')),('scale',StandardScaler()),
       ('pca',PCA(n_components=components,svd_solver='full')),('cluster',KMeans(n_clusters=clusters,n_init=10,random_state=seed))])
    pop_labels=pipe.fit_predict(a);customer_labels=pipe.predict(b)
    pop=np.bincount(pop_labels,minlength=clusters)/len(a)
    cust=np.bincount(customer_labels,minlength=clusters)/len(b)
    return pipe,pd.DataFrame({'cluster':range(clusters),'population_share':pop,'customer_share':cust,
      'representation_ratio':np.divide(cust,pop,out=np.full(clusters,np.nan),where=pop>0)})

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('population',type=Path);p.add_argument('customers',type=Path);p.add_argument('--clusters',type=int,default=10);args=p.parse_args()
    _,summary=segment(pd.read_csv(args.population),pd.read_csv(args.customers),clusters=args.clusters)
    print(summary.to_json(orient='records',indent=2))
