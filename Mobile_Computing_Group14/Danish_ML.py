import pandas as pd
from pandas import *
import xlrd
import os
import math
import pdb
import numpy as np
from numpy import dot
from numpy.linalg import norm




#test_file = pd.read_csv(r'C:\Users\Danish\Desktop\Excel Files\test_file.csv')


test_file = pd.read_csv(r'C:\Users\Danish\Desktop\MC A1\Mobile_Computing_Group14\uploads\key_points.csv')

def normalize(curr_file):
    rWX1 = curr_file['rightWrist_x'];
    rWY1 = curr_file['rightWrist_y'];
    nX1 = curr_file['nose_x'];
    nY1 = curr_file['nose_y'];
    lShX1 = curr_file['leftShoulder_x'];
    rShX1 = curr_file['rightShoulder_x'];
    hY1 = curr_file['leftHip_y'];
    rWXN = (rWX1 - nX1)/(abs(lShX1 - rShX1));
    rWYN = (rWY1 - nY1)/(abs(nY1-hY1));
    
    rWXNi=rWXN.dropna().reset_index(drop=True)
    rWYNi=rWYN.dropna().reset_index(drop=True)
    return [rWXNi,rWYNi]
    
        
def cosine_score(curr_file,test_file):
    curr_file=curr_file.dropna().reset_index(drop=True)
    test_file=test_file.dropna().reset_index(drop=True)
    #print("The Type of curr_file is",type(curr_file))
    #print("The Type of test_file is",type(test_file))
    
    [rWXNi,rWYNi] = normalize(curr_file)
    [rWXNT,rWYNT] = normalize(test_file)
    
 
    

    tAi = rWXNi*rWXNi+rWYNi*rWYNi;
    #print("The Type of rWXNi is",type(rWXNi))
    #print("The Type of rWYNi is",type(rWYNi))
    #print("/////")

    #print("The Type of rWXNT is",type(rWXNT))
    #print("The Type of rWYNT is",type(rWYNT))

    
    #[rWXNi,rWYNi]=[rWXNi.to_list(),rWYNi.to_list()]
    #print("The Type of rWXNi is",type(rWXNi))
    #print("The Type of rWYNi is",type(rWYNi))


    #[rWXNT,rWYNT]=[rWXNT.to_list(),rWYNT.to_list()]
    #print(rWXNT)
    #print("The Type of rWXNT is",type(rWXNT))
    #print("The Type of rWYNT is",type(rWYNT))
    
    
    
    
    #tAi = sum(a*a for a in rWXNi)+sum(b*b for b in rWYNi)
    
    
    tAT = rWXNT*rWXNT+rWYNT*rWYNT;
    #tAT = sum(a*a for a in rWXNT)+sum(b*b for b in rWYNT)


    #print(type(tAi))
    
    a1=min(len(tAi),len(tAT))
    a2=max(len(tAi),len(tAT))

    #a2 = 85
    # a1 = 55
    if(len(tAi)>len(tAT)):
        tAi = tAi[(a2-a1):]
        tAi=tAi.reset_index(drop = True)
        
    else:
        tAT = tAT[(a2-a1):]
        tAT=tAT.reset_index(drop = True)
        

    cos_sim = np.dot(tAi,tAT)/(np.sqrt(np.dot(tAi,tAi))*np.sqrt(np.dot(tAT,tAT)))
    #cosine_score = sum(tAi*tAT)/(math.sqrt(sum(tAi*tAi))*(math.sqrt(sum(tAT*tAT))))
    return cos_sim

#

d={};
count = 0;
directory_name = (r'C:\Users\Danish\Desktop\MC A1\Mobile_Computing_Group14\Excel Files');

for category_name in os.listdir(directory_name):
    path = os.path.join(directory_name, category_name)
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path):
            curr_file = pd.read_csv(file_path);
            curr_ans = cosine_score(curr_file,test_file);
            d[curr_ans] = category_name + str(count);
            count+=1
ans = dict(sorted(d.items()));
sub_ans = (list(ans.items())[-5:][::-1]);



temp={"programming": 0,
      "hardware": 0,
      "data": 0,
      "networking": 0,
      "cryptography":0
      }
for mix_word in sub_ans:
    s="";
    for word in mix_word[1]:
        if (ord(word)>=65 and ord(word)<=90) or (ord(word)>=97 and ord(word)<=122):
            s+=word;
    temp[s] = max(temp[s], mix_word[0])



print("Danish:",max(temp, key=temp.get))


            






