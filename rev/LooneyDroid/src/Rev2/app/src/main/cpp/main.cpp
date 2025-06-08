#include <jni.h>
#include <string>
#include <unistd.h>
#include "checker.h"
#include "base64.h"

jstring decodeMessage(JNIEnv* env, jobject thiz, jstring msg) {
    if (msg == NULL) {
        // Hello my buddy, what's your favourite cartoon?
        return env->NewStringUTF(base64_decode("SGVsbG8gbXkgYnVkZHksIHdoYXQncyB5b3VyIGZhdm91cml0ZSBjYXJ0b29uPw=="));
    }

    const char* cartoon = env->GetStringUTFChars(msg, nullptr);

    // Ooohh! I didn't expect that your favourite cartoon is:
    std::string result = base64_decode("T29vaGghIEkgZGlkbid0IGV4cGVjdCB0aGF0IHlvdXIgZmF2b3VyaXRlIGNhcnRvb24gaXM6IA==") + ((std::string)cartoon);
    env->ReleaseStringUTFChars(msg, cartoon);

    return env->NewStringUTF(result.c_str());
}

// Function to perfom the encryption
/*inline std::string encode(JNIEnv *env, std::string plain, const std::string key) {
    jclass clazz = env->FindClass("com/tnemesis/rev2/models/Crypto");
    jmethodID method = env->GetStaticMethodID(clazz, "defaultEncrypt", "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;");

    jstring encrypted = (jstring) env->CallStaticObjectMethod(
            clazz,
            method,
            env->NewStringUTF(plain.c_str()),
            env->NewStringUTF(key.c_str())
    );

    const char* chars = env->GetStringUTFChars(encrypted, nullptr);
    std::string result(chars);
    env->ReleaseStringUTFChars(encrypted, chars);

    return result;
}*/

inline std::string decode(JNIEnv *env, const std::string key) {
    jclass clazz = env->FindClass("com/tnemesis/rev2/models/Crypto");
    jmethodID method = env->GetStaticMethodID(clazz, "defaultDecrypt", "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;");

    jstring decripted = (jstring) env->CallStaticObjectMethod(
        clazz,
        method,
        env->NewStringUTF("F8wvI61iS+4DkaYRVE8+vElfo/C9PqIS6E8ESCfE+Y8mnHmZqVXDhmFnpMrsPKMs"),
        env->NewStringUTF(key.c_str())
    );

    const char* chars = env->GetStringUTFChars(decripted, nullptr);
    std::string result(chars);
    env->ReleaseStringUTFChars(decripted, chars);

    return result;
}

jstring decodeFlag(JNIEnv* env, jobject thiz, jstring msg) {
    if (msg == NULL) {
        // Hello my buddy, tell me your favourite cartoon!
        return env->NewStringUTF("SGVsbG8gbXkgYnVkZHksIHRlbGwgbWUgeW91ciBmYXZvdXJpdGUgY2FydG9vbiE=");
    }

    const char* cartoon = env->GetStringUTFChars(msg, nullptr);

    // Good choice! My favourite is:
    std::string result = ((std::string)base64_decode("R29vZCBjaG9pY2UhIE15IGZhdm91cml0ZSBpczog==")) + decode(env, cartoon);
    env->ReleaseStringUTFChars(msg, cartoon);

    return env->NewStringUTF(result.c_str());
}

JNIEXPORT jint JNI_OnLoad(JavaVM* vm, void* reserved) {
    JNIEnv* env;
    if (vm->GetEnv(reinterpret_cast<void**>(&env), JNI_VERSION_1_6) != JNI_OK) {
        return JNI_ERR;
    }

    char *ldfails = "/data/data/com.tnemesis.rev2/looney_droids.fails";
    if (access(ldfails, F_OK) == 0) {
        return JNI_VERSION_1_6;
    } else {
        // Create it in the first execution after installation
        FILE* file_ptr = fopen(ldfails, "w");
        fclose(file_ptr);
    }

    // just for testing
    // std::string encoded = encode(env, "N0PS{l00n3y_t00ns_or_l00n3y_dr01ds}", "looney_droids");  // base64_encode(encode("N0PS{l00n3y_t00ns_or_l00n3y_dr01ds}", "looney_droids").c_str(), 35);
    // std::string decoded = decode(env, "looney_droids");

    // Find your class. JNI_OnLoad is called from the correct class loader context for this to work.
    jclass c = env->FindClass("com/tnemesis/rev2/components/RandomReceiver");
    if (c == nullptr) return JNI_ERR;

    // Register your class' native methods.
    JNINativeMethod methods[1] = {{"decodeMessage", "(Ljava/lang/String;)Ljava/lang/String;"}};
    if (isDeviceSafe(env)) {
        methods[0].fnPtr = reinterpret_cast<void*>(decodeFlag);
    } else {
        methods[0].fnPtr = reinterpret_cast<void*>(decodeMessage);
    }

    int rc = env->RegisterNatives(c, methods, 1);
    if (rc != JNI_OK) return rc;

    return JNI_VERSION_1_6;
}

extern "C"
JNIEXPORT jstring JNICALL
Java_com_tnemesis_rev2_components_RandomReceiver_decodeMessage(JNIEnv *env, jclass clazz,
                                                               jstring message) {
    // "Your favourite cartoon is too boring"
    return env->NewStringUTF(base64_decode("WW91ciBmYXZvdXJpdGUgY2FydG9vbiBpcyB0b28gYm9yaW5n"));
}