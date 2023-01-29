package com.morrisz1.hackathon;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;

import com.google.android.material.textfield.TextInputLayout;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Calendar;


public class MainActivity extends AppCompatActivity {




    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void onDone(View view) {
        TextInputLayout carbsInputLayout = findViewById(R.id.carbs_Text);
        TextInputLayout insulinInputLayout = findViewById(R.id.insulin_Text);
        String carb = String.valueOf(carbsInputLayout.getEditText().getText());
        String insulin= String.valueOf(insulinInputLayout.getEditText().getText());
        DateFormat df = new SimpleDateFormat("yyyy,MM,dd HH:mm:ss z");
        String date = df.format(Calendar.getInstance().getTime());

    }

    public void onCancel(View view) {
        TextInputLayout carbsInputLayout = findViewById(R.id.carbs_Text);
        TextInputLayout insulinInputLayout = findViewById(R.id.insulin_Text);
        carbsInputLayout.getEditText().getText().clear();
        insulinInputLayout.getEditText().getText().clear();
    }
}