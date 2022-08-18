import os
import numpy as np
import pandas as pd


def normalize_dataset(frame):
    rightWrist_x, rightWrist_y = frame['rightWrist_x'], frame['rightWrist_y']
    nose_x, nose_y = frame['nose_x'], frame['nose_y']
    leftShoulder_x, rightShoulder_x, leftHip_y = frame['leftShoulder_x'], frame['rightShoulder_x'], frame['leftHip_y']

    rightWrist_normalise_x = ((rightWrist_x - nose_x) / abs(leftShoulder_x - rightShoulder_x)).dropna().reset_index(
        drop=True)
    rightWrist_normalise_y = ((rightWrist_y - nose_y) / abs(nose_y - leftHip_y)).dropna().reset_index(drop=True)

    return rightWrist_normalise_x, rightWrist_normalise_y


def cosine_similarity(curr_frame, test_frame):
    rightWrist_normalise_xi, rightWrist_normalise_yi = normalize_dataset(curr_frame)
    rightWrist_normalise_x_test, rightWrist_normalise_y_test = normalize_dataset(test_frame)

    trajectory_i = rightWrist_normalise_xi * rightWrist_normalise_xi + rightWrist_normalise_yi * rightWrist_normalise_yi;
    trajectory_test = rightWrist_normalise_x_test * rightWrist_normalise_x_test + rightWrist_normalise_y_test * rightWrist_normalise_y_test;

    difference_in_dataset = max(len(trajectory_i), len(trajectory_test)) - min(len(trajectory_i), len(trajectory_test))

    if len(trajectory_i) > len(trajectory_test):
        trajectory_i = trajectory_i[difference_in_dataset:].reset_index(drop=True)
    else:
        trajectory_test = trajectory_test[difference_in_dataset:].reset_index(drop=True)

    deno_product = np.sqrt(np.dot(trajectory_i, trajectory_i)) * np.sqrt(np.dot(trajectory_test, trajectory_test))

    cosine_score = np.dot(trajectory_i, trajectory_test) / deno_product

    return cosine_score


def algo_singh():
    prediction_dict = {}
    directory_name = r'C:\Users\Danish\Desktop\MC A1\Mobile_Computing_Group14\Excel Files'
    test_frame = pd.read_csv(r'C:\Users\Danish\Desktop\MC A1\Mobile_Computing_Group14\uploads\key_points.csv')

    for category_name in os.listdir(directory_name):
        category_list = []
        path = os.path.join(directory_name, category_name)
        for file_name in os.listdir(path):
            file_path = os.path.join(path, file_name)
            if os.path.isfile(file_path):
                curr_frame = pd.read_csv(file_path)
                category_list.append(cosine_similarity(curr_frame, test_frame))
        prediction_dict[category_name] = sorted(category_list)

    max_similar_gesture = {}
    for key, gesture_list in prediction_dict.items():
        max_similar_gesture[key] = gesture_list[-3:]

    prediction_list = {}
    for key, value in max_similar_gesture.items():
        prediction_list[key] = max(value)
        
    prediction = max(prediction_list, key=prediction_list.get)
    print(f'Tanuj:{prediction}')


algo_singh()

    
    
