import os
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, send_file, render_template, jsonify
import js2py
import shutil
import json
import numpy as np

UPLOAD_FOLDER = 'uploads/'
GESTURES_FOLDER = "ExpertGesture-1/"

# app = Flask(__name__)
app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
gestureCountDict = {}
gestureFileDict = {}
gestureNameDict = {}
nameGestureDict = {}


def initialize_expert_GestureFile():
    global gestureFileDict
    gestureFileDict = {'H0': 'h0.mp4', 'H1': 'h1.mp4', 'H2': 'h2.mp4', 'H3': 'h3.mp4', 'H4': 'h4.mp4', 'H5': 'h5.mp4',
                       'H6': 'h6.mp4', 'H7': 'h7.mp4', 'H8': 'h8.mp4', 'H9': 'h9.mp4', 'H10': 'h10.mp4',
                       'H11': 'h11.mp4', 'H12': 'h12.mp4', 'H13': 'h13.mp4', 'H14': 'h14.mp4', 'H15': 'h15.mp4',
                       'H16': 'h16.mp4', 'H17': 'h17.mp4', 'H18': 'h18.mp4', 'H19': 'h19.mp4', 'H20': 'h20.mp4',
                       'H21': 'h21.mp4', 'H22': 'h22.mp4', 'H23': 'h23.mp4', 'H24': 'h24.mp4', 'H25': 'h25.mp4',
                       'H26': 'h26.mp4', 'H27': 'h27.mp4', 'H28': 'h28.mp4', 'H29': 'h29.mp4', 'H30': 'h30.mp4',
                       'H31': 'h31.mp4', 'H32': 'h32.mp4', 'H33': 'h33.mp4', 'H34': 'h34.mp4', 'H35': 'h35.mp4',
                       'H36': 'h36.mp4', 'H37': 'h37.mp4', 'H38': 'h38.mp4', 'H39': 'h39.mp4', 'H40': 'h40.mp4',
                       'H41': 'h41.mp4', 'H42': 'h42.mp4', 'H43': 'h43.mp4', 'H44': 'h44.mp4'}

    global gestureNameDict
    gestureNameDict = {"H0": "ACPower",
                       "H1": "Algorithm",
                       "H2": "Antenna",
                       "H3": "Authentication",
                       "H4": "Authorization",
                       "H5": "Bandwidth",
                       "H6": "Bluetooth",
                       "H7": "Browser",
                       "H8": "Cloudcomputing",
                       "H9": "GDataCompression",
                       "H10": "DataLinkLayer",
                       "H11": "DataMining",
                       "H12": "Decryption",
                       "H13": "Domain",
                       "H14": "Email",
                       "H15": "Exposure",
                       "H16": "Filter",
                       "H17": "Firewall",
                       "H18": "Flooding",
                       "H19": "Gateway",
                       "H20": "Hacker",
                       "H21": "Header",
                       "H22": "HotSwap",
                       "H23": "Hyperlink",
                       "H24": "Infrastructure",
                       "H25": "Integrity",
                       "H26": "Internet",
                       "H27": "Intranet",
                       "H28": "Latency",
                       "H29": "Loopback",
                       "H30": "Motherboard",
                       "H31": "Network",
                       "H32": "Networking",
                       "H33": "Networklayer",
                       "H34": "Node",
                       "H35": "Packet",
                       "H36": "Partition",
                       "H37": "PasswordSniffing",
                       "H38": "Patch",
                       "H39": "Phishing",
                       "H40": "PhysicallLayer",
                       "H41": "Ping",
                       "H42": "Portscan",
                       "H43": "PresentationalLayer",
                       "H44": "Protocol"}

    global nameGestureDict;
    nameGestureDict = {gestureNameDict[name]: name for name in gestureNameDict}


def initialize_count_dict():
    if (not os.path.exists(UPLOAD_FOLDER)):
        os.mkdir(UPLOAD_FOLDER)
    for file in os.listdir(UPLOAD_FOLDER):
        if (file.endswith(".mp4")):
            file = file[:len(file) - 4].split("_")
            number = int(file[2])
            gesture = nameGestureDict[file[0]]
            name = "_".join(file[3:])
            if gesture not in gestureCountDict:
                gestureCountDict[gesture] = {}
            gestureCountDict[gesture][name] = max(number, gestureCountDict[gesture].get(name, 0))


def get_gesture_file_name(gesture_name, user_name):
    if gesture_name not in gestureCountDict:
        gestureCountDict[gesture_name] = {}
    gestureCountDict[gesture_name][user_name] = gestureCountDict[gesture_name].get(user_name, 0) + 1
    return "{}_PRACTICE_{}_{}.mp4".format(gestureNameDict[gesture_name], gestureCountDict[gesture_name][user_name],
                                          user_name)


def conversion():
    if (os.path.exists(r'C:\Users\Danish\Desktop\MC A1\Mobile_Computing_Group14\uploads\key_points.csv')):
        os.remove(r'C:\Users\Danish\Desktop\MC A1\Mobile_Computing_Group14\uploads\key_points.csv')
        print("file deleted")
    exec(open("Frames_Extractor.py").read())
    print("Frames Extracted")

    os.system('node scale_to_videos.js')

    print("Json File Created")
    os.system("python .\convert_to_csv.py")
    print("csv file created")

    os.system("python .\Danish_ML.py")
    os.system("python .\Ayush_ML.py")
    os.system("python .\Tanuj_ML.py")
    os.system("python .\Meghana_ML.py")


@app.route('/uploadGesture/<gesture_name>/<name>', methods=['GET', 'POST'])
def upload_file(gesture_name, name):
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify('no file'), 404
        file = request.files['file']
        filename = secure_filename(get_gesture_file_name(gesture_name, name))
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        conversion();

    return jsonify(success=True, message="Gesture Uploaded Successfully"), 200


@app.route('/getGesture/<gesture_name>', methods=['GET'])
def get_gesture(gesture_name):
    file_path = GESTURES_FOLDER + gestureFileDict[gesture_name]
    return send_file(file_path)


if __name__ == "__main__":
    initialize_expert_GestureFile()
    initialize_count_dict()
    app.run(host='172.20.10.6', port=1103)
