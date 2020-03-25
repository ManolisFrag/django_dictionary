import numpy as np
import pandas as pd
import random
import re
import os
import os.path
from HSL import Handshape
import math
# from scipy import stats
from HSL import Handshape
from tslearn.metrics import dtw_path, dtw_subsequence_path, dtw, soft_dtw
from tslearn.metrics import dtw as tsdtw
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
from scipy.ndimage import gaussian_filter, median_filter




def path_dtw(df, selected_sign):

    one_sign_coordinates_hand = []
    rest_sign_coordinates_hand = []
    for locc, folder in enumerate (df.Sequence.unique()):
        other_sign_video_path = df.loc[df['Sequence'] == folder]["Dominant_hand"].reset_index(drop=True)
        rest_sign_coordinates_hand.append(other_sign_video_path)

    
    # sign_video_path = selected_sign.reshape((int(len(selected_sign)/2),2))

    ex1 = selected_sign
    one_sign_coordinates_hand.append(ex1)            
    one_sign_path_dist = np.empty([len(rest_sign_coordinates_hand)])
    
    n = 5
    # ex1 = one_sign_coordinates_hand[0]
    # ex1 = np.hstack(ex1.astype(object).values)
    # ex1 = ex1.reshape((int(len(ex1)/2),2))
#     print(ex1)
    
    ex1 = median_filter(ex1,size=3, mode="wrap")
#     ex1 = gaussian_filter(ex1, sigma=1)
#     ex1 = stats.zscore(ex1)
#     ex1 = ex1[n:-n]



    for i in range(len(rest_sign_coordinates_hand)):

        ex2 = np.array(rest_sign_coordinates_hand[i].values.tolist())

        ex2 = ex2.reshape((len(ex2),2))
#         print(ex2.shape)
        
        
        ex2 = median_filter(ex2, size=3, mode="wrap")
#         ex2 = gaussian_filter(ex2, sigma=1)
#         ex2 = stats.zscore(ex2)
#         ex2 = ex2[n:-n]


        #old
#         one_sign_path_dist[i], _ = similaritymeasures.dtw(ex1, ex2)

        #new
        one_sign_path_dist[i]= soft_dtw(ex1,ex2)

#         one_sign_path_dist[i]= dtw(ex1,ex2, global_constraint="sakoe_chiba",sakoe_chiba_radius=2)

#         _, one_sign_path_dist[i] = dtw_subsequence_path(ex2,ex1)
        
        #test gak
#         one_sign_path_dist[i] = gak(ex1,ex2)
        
#         one_sign_path_dist[i] = directed_hausdorff(ex1, ex1)[0]
  
    columns_to_show=[]
    for i in df.Sequence.unique():
        i = i.split("/openpose/")[-1]
        columns_to_show.append(i)
        # line.split('_', 1)[-1]

    # scaled_values = one_sign_path_dist[:10] / sum(one_sign_path_dist[:10])
    # print("VALUES",one_sign_path_dist)

    one_sign_path_dist_df = pd.DataFrame(data=one_sign_path_dist, index=columns_to_show)
    only_first_ten_signs = one_sign_path_dist_df.sort_values(by=0)[:10]
    only_first_ten_signs = (only_first_ten_signs / sum(only_first_ten_signs[:].values))*100
    # print("all df: ",only_first_ten_signs)
    # print("only values:", only_first_ten_signs[:].values)

    return(only_first_ten_signs)