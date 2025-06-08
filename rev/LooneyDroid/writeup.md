## Looney Droids

### Description
As MJ, Jojo has been captured by the looney! To escape, he must win the game of the best cartoon...

**Author : Antonio Ruggia**  

**Challenge designed by [ThreatNemesis](https://tnemesis.com/)**

### Writeup
The app has two entry-points: MainActivity and RandomReceiver.
The receiver can be contacted via an intent with the `com.tnemesis.rev2.B3ST_C4RTOON` action and he pass the extra with key `cartoon` to a native function.

At the loading of the native library, the app performs anti-root (in Java) and anti-frida controls (in C++).
Only if all checks fail, the JNI_OnLoad function does the binding with the correct function (`decodeFlag`).
This function decode the flag with a AES-based encryption, whose key is the best cartoon: `looney_droids` (title of the challenge).

Moreover, at the first run, the app creates the file `/data/data/com.tnemesis.rev2/looney_droids.fails`.
If such a file is present, the native code does not verify the device (i.e., no binding with the `decodeFlag`).

Frida script example:
```javascript
// Avoid file existence check
let evade = false;
Interceptor.attach(Module.findExportByName("libc.so", "access"), {
    onEnter: function (args) {
        var path = Memory.readUtf8String(args[0]);
        evade = (path === "/data/data/com.tnemesis.rev2/looney_droids.fails");
    },
    onLeave: function (retval) {
        if (evade === true) {
            retval.replace(-1);
            console.log("[*] access() returned: " + retval.toInt32());
        } 
    }
});

var is_librev2 = 0
Interceptor.attach(Module.findExportByName(null, 'android_dlopen_ext'),{
    onEnter: function(args){
        var library_path = Memory.readCString(args[0]);
        is_librev2 = library_path.endsWith("librev2.so");
    },
    onLeave: function(args){
        if(is_librev2 === true){
            var librev2 = Process.findModuleByName("librev2.so");
            var exports = librev2.enumerateExports();
            for (var i = 0; i < exports.length; i++) {
                var symbol = exports[i];
                var address = symbol.address;
                if (symbol.name.indexOf("isDeviceSafe") >= 0 && symbol.name.endsWith("JNIEnv")) {
                    Interceptor.attach(address, {
                        onEnter: function (args) {
                        },
                        onLeave: function(retval) {
                            // console.log("isDeviceSafe result: ", retval);
                            retval.replace(1);
                        }
                    });
                } else if (symbol.name === "JNI_OnLoad") {
                    Interceptor.attach(address, {
                        onEnter: function (args) {},
                        onLeave: function(retval) {}
                    });
                }
            }
        }
    }
})
```

Procedure:
* Launch app with frida : `frida -U -f com.tnemesis.rev2 -l solve.js`
* Launch broadcast: `adb shell am broadcast -a com.tnemesis.rev2.B3ST_C4RTOON --es cartoon "looney_droids" -n com.tnemesis.rev2/.components.RandomReceiver`

Flag: `N0PS{l00n3y_t00ns_or_l00n3y_dr01ds}`