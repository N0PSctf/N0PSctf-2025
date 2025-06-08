package com.tnemesis.rev2;

import com.tnemesis.rev2.models.Checker;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.util.ArrayList;
import java.util.List;

public class Application extends android.app.Application {
    static final List<Boolean> checks = new ArrayList<>();

    @Override
    public void onCreate() {
        super.onCreate();

        Checker c = new Checker(this);
        for (Method m : c.getClass().getDeclaredMethods()) {
            if (!Modifier.isPublic(m.getModifiers())) {
                continue;
            }

            if (m.getName().startsWith("detect") || m.getName().startsWith("check")) {
                try {
                    checks.add((Boolean) m.invoke(c));
                } catch (IllegalAccessException | InvocationTargetException e) {
                    throw new RuntimeException(e);
                }
            }
        }

    }
}
