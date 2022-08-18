import math
import os
import pdb
import pandas as pd
from pandas import *
## importing algo libraries
import numpy as np




# getting cosine similarity value
def meghana_get_cosine_score(curr_file,video_file):
    video_file=video_file.dropna().reset_index(drop=True)
    curr_file=curr_file.dropna().reset_index(drop=True)
    
    [RightWristNormalize_Xi,RightWristNormalize_Yi] = meghana_normalize(curr_file);
    [RightWristNormalize_XT,RightWristNormalize_YT] = meghana_normalize(video_file);
    
    t_traj = RightWristNormalize_XT*RightWristNormalize_XT+RightWristNormalize_YT*RightWristNormalize_YT;
    i_traj = RightWristNormalize_Xi*RightWristNormalize_Xi+RightWristNormalize_Yi*RightWristNormalize_Yi;

    max_traj=max(len(i_traj),len(t_traj))
    min_traj=min(len(i_traj),len(t_traj))

    if(len(i_traj)<len(t_traj)):
        t_traj = t_traj[(max_traj-min_traj):]
        t_traj=t_traj.reset_index(drop = True)
        
    else:
        i_traj = i_traj[(max_traj-min_traj):]
        i_traj=i_traj.reset_index(drop = True)
        

    upper_value= np.dot(i_traj,t_traj)
    lower_value=np.sqrt(np.dot(i_traj,i_traj))*np.sqrt(np.dot(t_traj,t_traj))

    similarity_cosine_value =upper_value/lower_value
    return similarity_cosine_value


def meghana_algo():
    # gestures category list excel file path
    directory_name = (r'C:\Users\Danish\Desktop\MC A1\Mobile_Computing_Group14\Excel Files');

    ans={};
    for gesture_category in os.listdir(directory_name):
        path = os.path.join(directory_name, gesture_category)
        ans[gesture_category]=0;
        for file_name in os.listdir(path):
            csv_path = os.path.join(path, file_name)
            if os.path.isfile(csv_path):
                curr_file=pd.read_csv(csv_path);
                ans[gesture_category]=max(ans[gesture_category],meghana_get_cosine_score(curr_file,video_file))

    print("Meghana:",max(ans, key=ans.get))

## Geting normilized values from csv file
def meghana_normalize(csv_file):
    Y_RightWrist = csv_file['rightWrist_y'];
    Y_Nose = csv_file['nose_y'];
    Y_LeftHip = csv_file['leftHip_y'];

    # right wrist y normalized values
    RightWristNormalize_Y = (Y_RightWrist - Y_Nose)/(abs(Y_Nose-Y_LeftHip));


    X_LeftShoulder = csv_file['leftShoulder_x'];
    X_RightShoulder = csv_file['rightShoulder_x'];
    X_RightWrist = csv_file['rightWrist_x'];
    X_LeftShoulder = csv_file['leftShoulder_x'];
    X_Nose = csv_file['nose_x'];
    X_RightShoulder = csv_file['rightShoulder_x'];

    # right wrist x normalized values
    RightWristNormalize_X = (X_RightWrist - X_Nose)/(abs(X_LeftShoulder - X_RightShoulder));

    RightWristNormalize_Y=RightWristNormalize_Y.dropna().reset_index(drop=True)
    RightWristNormalize_X=RightWristNormalize_X.dropna().reset_index(drop=True)
    
    return [RightWristNormalize_X,RightWristNormalize_Y]


# path of video frames csv file
video_file = pd.read_csv(r'C:\Users\Danish\Desktop\MC A1\Mobile_Computing_Group14\uploads\key_points.csv')


meghana_algo()
        

            






