import os
import pandas as pd
import numpy as np
import sys
import argparse
import itertools


# The input data should respect :
#
#   1) The first col of sub files should be the ID (which is normally the case)
#   2) The other col(s) are for non exclusive proba (they don't sum to one)
#   3) From file to file the order of ID should be the same 

cutoff_lo = 0.8
cutoff_hi = 0.2

parser = argparse.ArgumentParser(description='Auto stacking of submission files')
parser.add_argument('path', help="relative path to the submission folder")
parser.add_argument('stacking_method', help="mean or median")
args = parser.parse_args()

sub_path = args.path
stacking = args.stacking_method 


# Read and concatenate submissions
outs = [pd.read_csv(os.path.join(sub_path, f)) for f in os.listdir(sub_path)]


nb_files = len(outs)
nb_cols = len(outs[0].columns) - 1 
id_name = outs[0].columns[0]
listlabels = outs[0].columns[1:].values


for i in range(nb_files) : 
    if i == (nb_files-1) : break
    # normally the index should be the same (can be an hexa)
    if ( outs[i].columns[0] != outs[i+1].columns[0] ) :  
        print("The ID list of all files should be equal")
        sys.exit()

 

concat_sub = pd.concat(outs, axis=1)
id_col = concat_sub.iloc[:,0]
concat_sub = concat_sub.drop([id_name], axis=1)




Allcolumns = []
for i in range(nb_cols) :
    cols = []
    for j in range(nb_files): 
        cols.append(concat_sub.columns[i] + "_" + str(j))
    Allcolumns.append(cols)


concat_sub.columns = np.array(Allcolumns).flatten()




for j in range(nb_cols): 

    concat_sub[listlabels[j]+ "_mean"] = concat_sub[Allcolumns[j]].mean(axis=1)
    concat_sub[listlabels[j]+ "_median"] = concat_sub[Allcolumns[j]].median(axis=1)





for j in range(nb_cols): 

    if stacking=="mean" : 
        concat_sub[listlabels[j]] = concat_sub[listlabels[j] + "_mean"]
    if stacking=="median" : 
        concat_sub[listlabels[j]] = concat_sub[listlabels[j] + "_median"]



concat_sub["id"] = id_col
concat_sub[list(itertools.chain.from_iterable([["id"], listlabels]))].to_csv(stacking + 'from' + str(nb_files) + 'SubFiles.csv', index=False, float_format='%.6f')




