package com.assignment.gesture;

import android.Manifest;
import android.app.Activity;
import android.content.pm.PackageManager;
import android.util.Log;

import androidx.core.app.ActivityCompat;

public class Utils {
    public static void handlePermissions(Activity activity) {

        int storagePermission = ActivityCompat.checkSelfPermission(activity, Manifest.permission.WRITE_EXTERNAL_STORAGE);
        int REQUEST_EXTERNAL_STORAGE = 1;

        String[] PERMISSIONS = {
                Manifest.permission.READ_EXTERNAL_STORAGE,
                Manifest.permission.WRITE_EXTERNAL_STORAGE,
                Manifest.permission.MANAGE_EXTERNAL_STORAGE,
                Manifest.permission.CAMERA

        };

        if (storagePermission != PackageManager.PERMISSION_GRANTED) {
            Log.i("log", "Read/Write Permissions needed!");
        }

        ActivityCompat.requestPermissions(
                activity,
                PERMISSIONS,
                REQUEST_EXTERNAL_STORAGE
        );

        Log.i("log", "Permissions Granted!");

    }
}
