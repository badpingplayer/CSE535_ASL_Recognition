package com.assignment.gesture.constants;

public class AppConstants {
    public static final String GESTURE = "gesture";
    public static final String LAST_NAME = "NAME";
    public static final String SERVER_ENDPOINT  = "http://172.20.10.6:1103/";
    public static final String GET_GESTURE = SERVER_ENDPOINT+"getGesture/%s";
    public static final String UPLOAD_GESTURE = SERVER_ENDPOINT+"/uploadGesture/%s/%s";
    public static final String PORT = "5000";
    public static final int SIXTY_FOUR_K = 64*1024;
    public static final int VIDEO_PLAY_COUNT = 1;
    public static final String GESTURE_RECORDING_PATH = "registerForActivityResult";
}
