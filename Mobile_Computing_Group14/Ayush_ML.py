import pdb
import numpy as np
import pandas as pd
import os
import math




#normalization function
def fun_norm(file):

    wrist_x_right = file['rightWrist_x'];
    shoulder_x_right = file['rightShoulder_x'];
    x_ValueNose = file['nose_x'];
    wrist_y_right = file['rightWrist_y'];
    Y_ValueNose = file['nose_y'];
    shoulder_x_left = file['leftShoulder_x'];
    Y_ValueHip = file['leftHip_y'];
    wrist_y_rightN = (wrist_y_right - Y_ValueNose)/(abs(Y_ValueNose-Y_ValueHip));
    wrist_x_rightN = (wrist_x_right - x_ValueNose)/(abs(shoulder_x_left - shoulder_x_right));
    
    wrist_x_rightN=wrist_x_rightN.dropna().reset_index(drop=True)
    wrist_y_rightN=wrist_y_rightN.dropna().reset_index(drop=True)
    
    return [wrist_x_rightN,wrist_y_rightN]


test_file = pd.read_csv(r'C:\Users\Danish\Desktop\MC A1\Mobile_Computing_Group14\uploads\key_points.csv')




def calculation(path_i,path_test):
    numerator=np.dot(path_i,path_test)
    denominator=np.sqrt(np.dot(path_i,path_i))*np.sqrt(np.dot(path_test,path_test))
    value= numerator/denominator
    return value



        
def similarity_values(file_present,test_file):
    test_file=test_file.dropna().reset_index(drop=True)
    file_present=file_present.dropna().reset_index(drop=True)
 

    [wrist_x_rightNi,wrist_y_rightNi] = fun_norm(file_present);
  
    [wrist_x_rightNT,wrist_y_rightNT] = fun_norm(test_file);
    
    path_i = wrist_x_rightNi*wrist_x_rightNi+wrist_y_rightNi*wrist_y_rightNi;
    path_test = wrist_x_rightNT*wrist_x_rightNT+wrist_y_rightNT*wrist_y_rightNT;



  
    if(len(path_i)>len(path_test)):
        path_i = path_i[(max(len(path_i),len(path_test))-min(len(path_i),len(path_test))):]
        path_i=path_i.reset_index(drop = True)
        
    else:
        path_test = path_test[(max(len(path_i),len(path_test))-min(len(path_i),len(path_test))):]
        path_test=path_test.reset_index(drop = True)

    



    return calculation(path_i,path_test)
    

ans={}
def categorize_ayush():
    
    directory_name = (r'C:\Users\Danish\Desktop\MC A1\Mobile_Computing_Group14\Excel Files');
    
    for video_cat in os.listdir(directory_name):
    	path = os.path.join(directory_name, video_cat)
    	ans[video_cat]=0;
    	for file_name in os.listdir(path):
            file_path = os.path.join(path, file_name)
            if os.path.isfile(file_path):
                file_present=pd.read_csv(file_path);
                ans[video_cat]=max(ans[video_cat],similarity_values(file_present,test_file))

    print("Ayush: ",max(ans, key=ans.get))
            

categorize_ayush()





