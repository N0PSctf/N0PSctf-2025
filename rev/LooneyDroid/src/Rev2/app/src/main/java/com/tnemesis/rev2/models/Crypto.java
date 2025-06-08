package com.tnemesis.rev2.models;

import android.util.Base64;

import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class Crypto {
    private final String algorithm;
    private final String transformation;

    public Crypto() {
        this("AES", "AES/ECB/PKCS5Padding");
    }

    public Crypto(String algorithm, String transformation) {
        this.algorithm = algorithm;
        this.transformation = transformation;
    }

    private static String padKey(String input) {
        return String.format("%16s", input).replace(' ', '0');
    }

    public String encrypt(String plain, String key) {
        try {
            Cipher cipher = Cipher.getInstance(this.transformation);
            SecretKeySpec secretKeySpec = new SecretKeySpec(padKey(key).getBytes(), this.algorithm);
            cipher.init(Cipher.ENCRYPT_MODE, secretKeySpec);
            byte[] encryptedBytes = cipher.doFinal(plain.getBytes());
            return Base64.encodeToString(encryptedBytes, Base64.DEFAULT);
        } catch (Exception e) {
            return null;
        }
    }

    public String decrypt(String text, String key) {
        try {
            Cipher cipher = Cipher.getInstance(this.transformation);
            SecretKeySpec secretKeySpec = new SecretKeySpec(padKey(key).getBytes(), this.algorithm);
            cipher.init(Cipher.DECRYPT_MODE, secretKeySpec);
            byte[] encryptedBytes = Base64.decode(text, Base64.DEFAULT);
            byte[] decryptedBytes = cipher.doFinal(encryptedBytes);
            return new String(decryptedBytes);
        } catch (Exception e) {
            return null;
        }
    }

    public static String defaultEncrypt(String s, String key) {
        return (new Crypto()).encrypt(s, key);
    }

    public static String defaultDecrypt(String s, String key) {
        return (new Crypto()).decrypt(s, key);
    }
}
