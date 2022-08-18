package com.assignment.gesture;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.assignment.gesture.constants.AppConstants;

public class LoginActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        Button continue_btn = findViewById(R.id.continueBtn);
        TextView last_name = findViewById(R.id.lastName);
        continue_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String name = last_name.getText().toString();
                if(name!=null && name.length()>0){
                    Intent mainIntent = new Intent(getApplicationContext(),MainActivity.class);
                    mainIntent.putExtra(AppConstants.LAST_NAME,name);
                    startActivity(mainIntent);
                }else{
                    Toast.makeText(getApplicationContext(),"Please enter Last Name to continue",Toast.LENGTH_LONG).show();
                }
            }
        });
    }
}