package com.assignment.gesture;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;
import android.widget.VideoView;

import com.assignment.gesture.constants.AppConstants;
import com.assignment.gesture.constants.Gesture;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class PracticeView extends AppCompatActivity {

    private Bundle params;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_practice_view);
        VideoView demoVideoView =  (VideoView) findViewById(R.id.videoView);
        Button uploadButton = (Button)findViewById(R.id.upload_button);
        params = getIntent().getExtras()==null?new Bundle():getIntent().getExtras();
        File mediaFile = new File(params.getString(AppConstants.GESTURE_RECORDING_PATH));
        demoVideoView.setVideoURI(Uri.fromFile(mediaFile));
        demoVideoView.start();
        uploadButton.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                new UploadVideo().execute(params);
            }
        });
    }

    private class UploadVideo extends AsyncTask<Bundle, Float, Response> {

        @Override
        protected Response doInBackground(Bundle... bundles) {
            String postUrl = String.format(AppConstants.UPLOAD_GESTURE, params.getSerializable(AppConstants.GESTURE).toString(),params.getString(AppConstants.LAST_NAME,"dummy"));
            File stream = null;
            RequestBody postBodyImage = null;
            try {
                stream = new File(params.getString(AppConstants.GESTURE_RECORDING_PATH));
                postBodyImage = new MultipartBody.Builder()
                        .setType(MultipartBody.FORM)
                        .addFormDataPart("file",
                                stream.getName(), RequestBody.create(MediaType.parse("video/*"), stream))
                        .build();
                OkHttpClient client = new OkHttpClient();

                Request request = new Request.Builder()
                        .url(postUrl)
                        .post(postBodyImage)
                        .build();
                Response response = client.newCall(request).execute();
                return response;

            } catch (Exception ioexp) {
                ioexp.printStackTrace();
            }
            return null;
        }

        @Override
        protected void onPostExecute(Response response) {
            if(response!=null && response.code()==200){
                Toast.makeText(getApplicationContext(),"VIDEO Uploaded Successfully",Toast.LENGTH_LONG
                ).show();
                Intent intent =  new Intent(getApplicationContext(),MainActivity.class);
                intent.putExtras(params);
                startActivity(intent);
                return;
            }
            Toast.makeText(getApplicationContext(),"VIDEO upload Failed. Please Try Again",Toast.LENGTH_LONG
            ).show();
        }
    }
}