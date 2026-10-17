# Input contract

Provide population and customer CSVs with matching numeric feature columns. segment fits imputation, scaling, PCA, and K-means only on the population table, then projects customers into the same fitted space. The default retains 90% PCA variance; an explicit component count can be passed through the Python API. No original population/customer files, feature dictionary, profiles, or centroids are distributed.
