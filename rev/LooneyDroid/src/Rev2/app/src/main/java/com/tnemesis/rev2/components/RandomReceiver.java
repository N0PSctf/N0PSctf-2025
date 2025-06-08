package com.tnemesis.rev2.components;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

public class RandomReceiver extends BroadcastReceiver {
    static {
        System.loadLibrary("rev2");
    }

    public static native String decodeMessage(String message);

    @Override
    public void onReceive(Context context, Intent intent) {
        String cartoon = null;
        if (intent.hasExtra("cartoon")) {
            cartoon = intent.getStringExtra("cartoon");
        }

        String result = decodeMessage(cartoon);
        Intent response = new Intent(context.getApplicationContext(), MainActivity.class);
        response.putExtra("result", result);
        response.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        context.getApplicationContext().startActivity(response);
    }
}