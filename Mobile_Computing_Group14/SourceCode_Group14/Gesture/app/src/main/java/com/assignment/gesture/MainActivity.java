package com.assignment.gesture;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;

import com.assignment.gesture.constants.AppConstants;
import com.assignment.gesture.constants.Gesture;

import java.util.List;
import java.util.stream.Collectors;


public class MainActivity extends AppCompatActivity {
    @RequiresApi(api = Build.VERSION_CODES.N)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        final Gesture[] selectedGesture = {null};


        List<String> spinnerArray = Gesture.getGestures().stream().map(Gesture::getGesture).collect(Collectors.toList());

        Bundle params = getIntent().getExtras()==null?new Bundle():getIntent().getExtras();
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(
                this, android.R.layout.simple_spinner_item, spinnerArray);

        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        Spinner sItems = (Spinner) findViewById(R.id.gesture_drop_down);
        sItems.setAdapter(adapter);
        sItems.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int i, long l) {
                selectedGesture[0] = Gesture.getGesture(parent.getSelectedItem().toString());
            }

            @Override
            public void onNothingSelected(AdapterView<?> adapterView) {

            }
        });
        Button button = findViewById(R.id.check_gesture_button);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), ExpertView.class);
                params.putSerializable(AppConstants.GESTURE, selectedGesture[0]);
                intent.putExtras(params);
                startActivity(intent);
            }
        });
    }
}