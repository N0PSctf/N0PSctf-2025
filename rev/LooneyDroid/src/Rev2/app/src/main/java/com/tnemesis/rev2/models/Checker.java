package com.tnemesis.rev2.models;

import static com.tnemesis.rev2.models.Const.BINARY_SU;

import android.content.Context;
import android.content.pm.PackageManager;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Scanner;

public class Checker {
    private static Context context;
    public Checker(Context context) {
        this.context = context;
    }
    // refactored RootBeer + random checks
    public boolean detectTestKeys() {
        String buildTags = android.os.Build.TAGS;
        return buildTags != null && buildTags.contains("test-keys");
    }

    public boolean detectRootManagementApps() {
        return isAnyPackageFromListInstalled(Arrays.asList(Const.knownRootAppsPackages));
    }

    public boolean detectPotentiallyDangerousApps() {
        return isAnyPackageFromListInstalled(Arrays.asList(Const.knownDangerousAppsPackages));
    }

    public boolean detectRootCloakingApps() {
        return isAnyPackageFromListInstalled(Arrays.asList(Const.knownRootCloakingPackages));
    }

    public boolean checkForSuBinary() {
        return checkForBinary(BINARY_SU);
    }

    public boolean checkForMagiskBinary() {
        return checkForBinary("magisk");
    }

    public boolean checkForBusyBoxBinary(){
        return checkForBinary("busybox");
    }

    private boolean checkForBinary(String filename) {

        String[] pathsArray = Const.getPaths();

        boolean result = false;

        for (String path : pathsArray) {
            // String completePath = path + filename;
            File f = new File(path, filename);
            boolean fileExists = f.exists();
            if (fileExists) {
                result = true;
            }
        }

        return result;
    }

    private boolean isAnyPackageFromListInstalled(List<String> packages){
        boolean result = false;

        PackageManager pm = this.context.getPackageManager();

        for (String packageName : packages) {
            try {
                pm.getPackageInfo(packageName, 0);
                result = true;
            } catch (PackageManager.NameNotFoundException e) {
                // Exception thrown, package is not installed into the system
            }
        }

        return result;
    }

    public boolean checkSuExists() {
        Process process = null;
        try {
            process = Runtime.getRuntime().exec(new String[] { "which", BINARY_SU });
            BufferedReader in = new BufferedReader(new InputStreamReader(process.getInputStream()));
            return in.readLine() != null;
        } catch (Throwable t) {
            return false;
        } finally {
            if (process != null) process.destroy();
        }
    }
}
