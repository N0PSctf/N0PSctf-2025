package com.tnemesis.rev2.components;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.content.BroadcastReceiver;
import android.os.Bundle;
import android.widget.TextView;

import com.tnemesis.rev2.databinding.ActivityMainBinding;

import java.io.File;

public class MainActivity extends AppCompatActivity {

    // Used to load the 'rev2' library on application startup.
    private ActivityMainBinding binding;

    @SuppressLint("SetTextI18n")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        // TODO: Make an interesting view

        // Create empty file
        try {
            File file = new File("/data/data/com.tnemesis.rev2/looney_droids.fails");
            file.createNewFile();
        } catch(Exception e) { /* ignore */ }

        // Example of a call to a native method
        TextView tv = binding.sampleText;

        String msg = "No interesting cartoon here.";
        if (this.getIntent().hasExtra("result")) {
            msg = this.getIntent().getStringExtra("result");
        }
        tv.setText(msg);
    }

}