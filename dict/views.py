from django.shortcuts import render
from django.http import HttpResponse 
import requests
import numpy as np
import pandas as pd
import random
import re
import os
import os.path
from HSL import Handshape
import math
from scipy import stats
from tslearn.metrics import dtw_path, dtw_subsequence_path, dtw, soft_dtw
from tslearn.metrics import dtw as tsdtw
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
from scipy.ndimage import gaussian_filter, median_filter
from signlib import misc2
from my_functions import path_dtw
from django.core.cache import cache
from django.db import router, transaction
from .forms import PoseForm
from .models import Pose_model
from django.contrib.staticfiles.storage import staticfiles_storage

# function to read all the contents from the dictionary and save them into a pickle file
def run_first_time():
    directory_of_dictionary = "./django_project/pose_dictionary"

    # create dataframe to store all information
    list_json_files = []
    list_dirs = []
    list_img_files = []
    df = pd.DataFrame(columns=['Sequence', 'Json_file' ,'Dominant_hand', 'Non_dominant_hand', 'Dominant_confidence', 'Non_dominant_confidence'])


    exclude = set(['.ipynb_checkpoints'])
    for dirpath, dirnames, filenames in os.walk(directory_of_dictionary, topdown=True):
        dirnames[:] = [d for d in dirnames if d not in exclude]
    #     print(dirnames)
        for filename in [f for f in filenames if f.endswith(".json")]:
            list_json_files.append(os.path.join(dirpath, filename))
            list_dirs.append(dirpath.replace('./data/', ''))
            
    list_json_files.sort()
    list_dirs.sort()

    df['Sequence'] = list_dirs
    df['Json_file'] = list_json_files
    
    for i in range(df.shape[0]):
    #     print(str(df['Json_file'].iloc[i]))
        
        dominant, non_dominant, dominant_confidence, non_dominant_confidence =  misc2.get_hands_from_json(str(df['Json_file'].iloc[i]))
        # fingers, conf = Handshape.handshape(str(df['Json_file'].iloc[i])).get_right_fingers_from_json
        # df['Fingers_coordinates'].iloc[i] = fingers
        df['Dominant_hand'].iloc[i] = dominant
        df['Non_dominant_hand'].iloc[i] = non_dominant
        df['Dominant_confidence'].iloc[i] = dominant_confidence
        df['Non_dominant_confidence'].iloc[i] = non_dominant_confidence

    df = df.drop(df.index[df["Dominant_confidence"] < 0.3].tolist())
    df.to_pickle(r'dict/static/dict/export_dataframe.pkl')


def button(request):

    return render(request,'home.html')

def output(request):
    #uncomment the line above only the first time to run the project in order to save all the data to a pickle file to make it faster
    # run_first_time()

    df = pd.read_pickle(r'dict/static/dict/export_dataframe.pkl')
    # print(df)
    #select the sign
    # retrieve the last saved array in the model database and save it to last_pose
    entries_model = Pose_model.objects.all()
    for fav in entries_model:
        last_pose = fav.pose_array
        q = fav

    
    last_pose = np.fromstring(last_pose, dtype=float, sep=',')
    last_pose = last_pose.reshape((int(len(last_pose)/2),2))
    

    # list_json_files_s = []
    # list_dirs_s = []
    # list_img_files_s = []
    # dicrectory_of_the_sign_to_search = "./django_project/testing_sign"
    # for dirpath_s, dirnames_s, filenames_s in os.walk(dicrectory_of_the_sign_to_search, topdown=True):
    #     dirnames_s[:] = [d for d in dirnames_s if d not in exclude]
    #     # print(dirnames)
    #     for filename in [f for f in filenames_s if f.endswith(".json")]:
    #         list_json_files_s.append(os.path.join(dirpath_s, filename))
    #         list_dirs_s.append(dicrectory_of_the_sign_to_search.replace('./data/', ''))
            
    # list_json_files_s.sort()
    # list_dirs_s.sort()

    # df_my_sign = pd.DataFrame(columns=['Sequence', 'Json_file','Dominant_hand', 'Non_dominant_hand', 'Dominant_confidence', 'Non_dominant_confidence'])
    # df_my_sign['Sequence'] = list_dirs_s
    # df_my_sign['Json_file'] = list_json_files_s

    # for i in range(df_my_sign.shape[0]):
    # #     print(str(df['Json_file'].iloc[i]))
        
    #     dominant, non_dominant, dominant_confidence, non_dominant_confidence =  misc2.get_hands_from_json(str(df_my_sign['Json_file'].iloc[i]))
    #     # fingers, conf = Handshape.handshape(str(df_my_sign['Json_file'].iloc[i])).get_right_fingers_from_json
    #     # df_my_sign['Fingers_coordinates'].iloc[i] = fingers
    #     df_my_sign['Dominant_hand'].iloc[i] = dominant
    #     df_my_sign['Non_dominant_hand'].iloc[i] = non_dominant
    #     df_my_sign['Dominant_confidence'].iloc[i] = dominant_confidence
    #     df_my_sign['Non_dominant_confidence'].iloc[i] = non_dominant_confidence
    # my_list_of_directories = []
    # not_last = []
    # root = "./django_project/output/"
    # first_dir= os.listdir(root) # get all files' and folders' names in the current directory
    # #print("First directory is: ",first_dir)

    # if used with openpose:
    # DataFrame = path_dtw(df, df_my_sign)

    #if used with posenet from the recorded Home.html 
    DataFrame = path_dtw(df, last_pose)
  
    # DELETE RECORDS IN DATABASE
    notes = entries_model.values_list("id", flat=True)[3:]
    Pose_model.objects.exclude(pk__in=list(notes)).delete()
    ############
    return render(request,'dict/about.html',{'DataFrame': DataFrame[0]})

def home(request):
    
    form = PoseForm(request.POST or None)
    if form.is_valid():
        form.save()

    context = {
        'form':form
    }  
    return render(request, 'dict/home.html',context)

def about(request):
    entries_model = Pose_model.objects.all()
    for fav in entries_model:
        p = fav.pose_array
        q = fav
    # print(q,p)
    # return render(request, 'dict/about.html', {'DataFrame': DataFrame[0]})
    
    return render(request, 'dict/about.html',{'poses': entries_model})
    # Pose_model.objects.all().delete()
    # return HttpResponse('entered text:', request.POST.get('place_for_table', True))

def return_data(request):
    return HttpResponse('entered text:' , request.POST.get('place_for_table', False))

def pose_create_view(request):
    form = PoseForm(request.POST or None)
    if form.is_valid():
        form.save()

    context = {
        'form':form
    }    

    return render(request,"dict/pose_view.html", context)
# Create your views here.
