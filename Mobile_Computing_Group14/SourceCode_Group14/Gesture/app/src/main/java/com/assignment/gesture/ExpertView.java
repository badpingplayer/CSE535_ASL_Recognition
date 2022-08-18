package com.assignment.gesture;

import androidx.activity.result.ActivityResultCallback;
import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.activity.result.ActivityResult;
import androidx.core.content.FileProvider;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.os.StrictMode;
import android.provider.MediaStore;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.VideoView;


import com.assignment.gesture.constants.AppConstants;
import com.assignment.gesture.constants.Gesture;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.lang.reflect.Method;
import java.util.concurrent.atomic.AtomicInteger;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class ExpertView extends AppCompatActivity {
    private AtomicInteger videoPlayCount;
    private String rootPath = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOCUMENTS).getPath();
    private Bundle params;
    private static int VIDEO_REQUEST =101;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_expert_view);
        videoPlayCount = new AtomicInteger(AppConstants.VIDEO_PLAY_COUNT);
        setVisibility();
        if (ContextCompat.checkSelfPermission(this,
                Manifest.permission.CAMERA)
                != PackageManager.PERMISSION_GRANTED) {
            if (ActivityCompat.shouldShowRequestPermissionRationale(this,
                    Manifest.permission.CAMERA)) {
            } else {
                ActivityCompat.requestPermissions(this,
                        new String[]{Manifest.permission.CAMERA},
                        101);
            }
        }
        if (ContextCompat.checkSelfPermission(this,
                Manifest.permission.WRITE_EXTERNAL_STORAGE)
                != PackageManager.PERMISSION_GRANTED) {
            if (ActivityCompat.shouldShowRequestPermissionRationale(this,
                    Manifest.permission.WRITE_EXTERNAL_STORAGE)) {
            } else {
                ActivityCompat.requestPermissions(this,
                        new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE},
                        100);
            }

        }
        Utils.handlePermissions(ExpertView.this);
        params = getIntent().getExtras()==null?new Bundle():getIntent().getExtras();
        ActivityResultLauncher<Intent> activityResultLauncher = registerForActivityResult(new ActivityResultContracts.StartActivityForResult(), new ActivityResultCallback<ActivityResult>() {
            @Override
            public void onActivityResult(ActivityResult result) {
                if(result.getResultCode() == RESULT_OK){
                    Toast.makeText(getApplicationContext(),"VIDEO Recorded Successfully",Toast.LENGTH_LONG
                    ).show();
                    Uri fileUri = result.getData().getData();
                    params.putString(AppConstants.GESTURE_RECORDING_PATH,fileUri.getPath());
                    Intent practiceIntent =  new Intent(getApplicationContext(),PracticeView.class);
                    practiceIntent.putExtras(params);
                    startActivity(practiceIntent);
                }
            }
        });
        VideoView demoVideoView = (VideoView) findViewById(R.id.videoView);
        Button playButton = (Button)findViewById(R.id.play_video_button);
        Button practiceButton = (Button)findViewById(R.id.practice_button);
        practiceButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent videoIntent = new Intent(MediaStore.ACTION_VIDEO_CAPTURE);
                if(Build.VERSION.SDK_INT>=24){
                    try{
                        Method m = StrictMode.class.getMethod("disableDeathOnFileUriExposure");
                        m.invoke(null);
                    }catch(Exception e){
                        e.printStackTrace();
                    }
                }
                File mediaFile = new File( rootPath + "/recording.mp4");
                videoIntent.putExtra(MediaStore.EXTRA_DURATION_LIMIT, 5);
                videoIntent.putExtra(MediaStore.EXTRA_OUTPUT, Uri.fromFile(mediaFile));
                videoIntent.setFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
                videoIntent.setFlags(Intent.FLAG_GRANT_WRITE_URI_PERMISSION);
//                videoIntent.putExtra("android.intent.extras.CAMERA_FACING", android.hardware.Camera.CameraInfo.CAMERA_FACING_FRONT);
//                videoIntent.putExtra("android.intent.extras.LENS_FACING_FRONT", 1);
//                videoIntent.putExtra("android.intent.extra.USE_FRONT_CAMERA", true);
                activityResultLauncher.launch(videoIntent);
            }
        });
        playButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(!demoVideoView.isPlaying()){
                    videoPlayCount.decrementAndGet();
                    setVisibility();
                    demoVideoView.start();
                }else{
                    Toast.makeText(getApplicationContext(),"Still Playing",Toast.LENGTH_LONG).show();
                }
            }
        });
        new DownloadVideo().execute((Gesture) params.getSerializable(AppConstants.GESTURE));
    }

    public void setVisibility(){
        Button uploadButton = (Button) findViewById(R.id.practice_button);
        uploadButton.setVisibility(this.videoPlayCount.get()<=0? View.VISIBLE:View.GONE);
        TextView textView = (TextView) findViewById(R.id.enable_practice);
        textView.setVisibility(this.videoPlayCount.get()<=0? View.GONE:View.VISIBLE);
    }


    private class DownloadVideo extends AsyncTask<Gesture, Float, Uri>{

        @Override
        protected Uri doInBackground(Gesture... gestures) {
            ((VideoView) findViewById(R.id.videoView)).stopPlayback();
            String postUrl = String.format(AppConstants.GET_GESTURE, gestures[0].toString());
            OkHttpClient client = new OkHttpClient();
            Request request =  new Request.Builder().url(postUrl).build();
            File targetFile = new File(rootPath+"/demo.mp4");
            while(targetFile.exists()){
                targetFile.delete();
            }
            try (Response response = client.newCall(request).execute()) {
                byte[] buffer = new byte[AppConstants.SIXTY_FOUR_K];
                InputStream initialStream = response.body().byteStream();
                OutputStream outStream = new FileOutputStream(targetFile);
                int bytesRead;
                while ((bytesRead = initialStream.read(buffer)) != -1) {
                    outStream.write(buffer, 0, bytesRead);
                }
                initialStream.close();
                outStream.close();
                return Uri.fromFile(targetFile);
            } catch (IOException e) {
                e.printStackTrace();
            }
            return null;
        }

        @Override
        protected void onPostExecute(Uri file) {
            Button playButton = (Button)findViewById(R.id.play_video_button);
            playButton.setVisibility(View.GONE);
            if(file!=null){
                ((VideoView)findViewById(R.id.videoView)).setVideoURI(file);
                playButton.setVisibility(View.VISIBLE);
            }
        }
    }
}