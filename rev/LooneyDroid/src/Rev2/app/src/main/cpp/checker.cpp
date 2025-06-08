//
// Created by Antonio on 27/02/2025.
//
#include <jni.h>
#include <jni.h>
#include <string>
#include <cstdlib>
#include <mntent.h>
#include <unistd.h>
#include <cstdio>
#include <fcntl.h>
#include <dirent.h>
#include <cstring>
#include <malloc.h>
#include <pthread.h>
#include <cctype>

#include <android/log.h>

#include <arpa/inet.h>

#include <sys/stat.h>
#include <sys/system_properties.h>
#include <sys/types.h>
#include <sys/prctl.h>
#include <sys/stat.h>
#include <asm/unistd.h>

#include <android/log.h>

// TODO: Check props

inline bool isFridaOpenPortNative() {
    bool result = false;

    for(int i = 0 ; i <= 65535 ; i++) {
        struct sockaddr_in sa;

        int sock = socket(AF_INET ,SOCK_STREAM, 0);
        sa.sin_port = htons(i);

        if (connect(sock , (struct sockaddr*)&sa , sizeof sa) != -1) {
            char res[8];
            memset(res, 0 , 7);

            send(sock, "\x00", 1, NULL);
            send(sock, "AUTH\r\n", 6, NULL);

            usleep(100);

            bool ret = (recv(sock, res, 6, MSG_DONTWAIT) != -1);
            if (ret) {
                // LOGD("Response %s", res);
                if (strcmp(res, "REJECT") == 0) {
                    /* Frida server detected. Do something… */
                    result = true;
                }
            }
        }

        close(sock);
        if (result)
            break;
    }

    return result;
}

static const char *FRIDA_THREAD_GUM_JS_LOOP = "gum-js-loop";
static const char *FRIDA_THREAD_GMAIN = "gmain";
static const char *FRIDA_NAMEDPIPE_LINJECTOR = "linjector";

static const char *PROC_MAPS = "/proc/self/maps";
static const char *PROC_STATUS = "/proc/self/task/%s/status";
static const char *PROC_FD = "/proc/self/fd";
static const char *PROC_TASK = "/proc/self/task";
static const char *PROC_TASK_MEM = "/proc/self/task/%s/mem";
static const char *PROC_TASK_PAGEMAP = "/proc/self/task/%s/pagemap";
static const char *PROC_SELF_PAGEMAP = "/proc/self/pagemap";
static const char *PROC_SELF_MEM = "/proc/self/mem";
static const char *PROC_COMM = "/proc/self/task/%s/comm";
static const char *PROC_SELF_STATUS = "/proc/self/status";

ssize_t readLine(int fd, char *buf, unsigned int max_len) {
    char b;
    ssize_t ret;
    ssize_t bytes_read = 0;
    memset(buf, 0, max_len);

    do {
        ret = read(fd, &b, 1);
        if (ret != 1) {
            if (bytes_read == 0) {
                // error or EOF
                return -1;
            } else {
                return bytes_read;
            }
        }
        if (b == '\n') {
            return bytes_read;
        }
        *(buf++) = b;
        bytes_read += 1;

    } while (bytes_read < max_len - 1);
    return bytes_read;
}

bool detectFridaThreadNative() {
    bool result = false;
    DIR *dir = opendir(PROC_TASK);

    if (dir != NULL) {
        struct dirent *entry = NULL;
        while ((entry = readdir(dir)) != NULL) {
        char filePath[PATH_MAX] = "";

        if (0 == strcmp(entry->d_name, ".") || 0 == strcmp(entry->d_name, "..")) {
            continue;
        }
        snprintf(filePath, sizeof(filePath), PROC_STATUS, entry->d_name);

        int fd = openat(AT_FDCWD, filePath, O_RDONLY | O_CLOEXEC, 0);
        // int fd = openat(AT_FDCWD, filePath, O_RDONLY | O_CLOEXEC, 0);
        if (fd != 0) {
            char buf[PATH_MAX] = "";
            readLine(fd, buf, (unsigned int) PATH_MAX);
            if (strstr(buf, FRIDA_THREAD_GUM_JS_LOOP) || strstr(buf, FRIDA_THREAD_GMAIN)) {
                result = true;
            }

            close(fd);
            if (result)
                break;
            }
        }
        closedir(dir);
    }

    return result;
}

bool detectFridaNamedPipeNative() {
    bool result = false;

    DIR *dir = opendir(PROC_FD);
    if (dir != NULL) {
        struct dirent *entry = NULL;
        while ((entry = readdir(dir)) != NULL) {
            struct stat filestat;
            char buf[PATH_MAX] = "";
            char filePath[PATH_MAX] = "";
            snprintf(filePath, sizeof(filePath), "/proc/self/fd/%s", entry->d_name);

            lstat(filePath, &filestat);

            if ((filestat.st_mode & S_IFMT) == S_IFLNK) {
                readlinkat(AT_FDCWD, filePath, buf, PATH_MAX);
                if (strstr(buf, FRIDA_NAMEDPIPE_LINJECTOR)) {
                    result = true;
                    break;
                }
            }
        }
    }
    closedir(dir);

    return result;
}

inline bool checkJavaControls(JNIEnv *env) {
    bool ret = false;
    jclass cls = env->FindClass("com/tnemesis/rev2/Application");
    jfieldID fieldID = env->GetStaticFieldID(cls, "checks", "Ljava/util/List;");
    jobject listObj = env->GetStaticObjectField(cls, fieldID);

    jclass listClass = env->FindClass("java/util/List");
    jmethodID sizeMethod = env->GetMethodID(listClass, "size", "()I");
    jmethodID getMethod = env->GetMethodID(listClass, "get", "(I)Ljava/lang/Object;");

    jint size = env->CallIntMethod(listObj, sizeMethod);
    jclass booleanClass = env->FindClass("java/lang/Boolean");
    jmethodID booleanValueMethod = env->GetMethodID(booleanClass, "booleanValue", "()Z");

    for (jint i = 0; i < size; i++) {
        jobject boolObj = env->CallObjectMethod(listObj, getMethod, i);
        jboolean value = env->CallBooleanMethod(boolObj, booleanValueMethod);
        if (value == true){
            ret = true;
        }
        env->DeleteLocalRef(boolObj);
        if (ret) {
            break;
        }
    }

    env->DeleteLocalRef(listObj);
    env->DeleteLocalRef(listClass);
    env->DeleteLocalRef(booleanClass);

    return ret;
}

bool isDeviceSafe(JNIEnv *env) {
    if (checkJavaControls(env)) {
        return false;
    }

    if (detectFridaNamedPipeNative() || detectFridaThreadNative() || isFridaOpenPortNative()) {
        return false;
    }

    return true;
}
