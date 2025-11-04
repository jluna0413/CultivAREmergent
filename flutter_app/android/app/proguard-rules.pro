# Add project specific ProGuard rules here.
# You can control the set of applied configuration files using the
# proguardFiles setting in build.gradle.kts.

# For more details, see
#   http://developer.android.com/guide/developing/tools/proguard.html

# If your project uses WebView with JS, uncomment the following
# and specify the fully qualified class name to the JavaScript interface
# class:
-keepclassmembers class fqcn.of.javascript.interface.for.webview {
   public *;
}

# Uncomment this to preserve the line number information for
# debugging stack traces.
-keepattributes SourceFile,LineNumberTable

# If you keep the line number information, uncomment this to
# hide the original source file name.
-renamesourcefileattribute SourceFile

# Keep Flutter related classes and methods
-keep class io.flutter.app.** { *; }
-keep class io.flutter.plugin.**  { *; }
-keep class io.flutter.util.**  { *; }
-keep class io.flutter.view.**  { *; }
-keep class io.flutter.**  { *; }
-keep class io.flutter.plugins.**  { *; }

# Keep Androidx annotations
-keep @androidx.annotation.Keep class *
-keep class android.annotation.** { *; }

# Preserve all serializable classes and their members
-keepnames class * implements java.io.Serializable
-keepclassmembers class * implements java.io.Serializable {
    static final long serialVersionUID;
    private static final java.io.ObjectStreamField[] serialPersistentFields;
    !static !transient <fields>;
    private void writeObject(java.io.ObjectOutputStream);
    private void readObject(java.io.ObjectInputStream);
    java.lang.Object writeReplace();
    java.lang.Object readResolve();
}

# Keep Enums
-keepclassmembers enum * {
    public static **[] values();
    public static ** valueOf(java.lang.String);
}

# Keep Parcelable implementations
-keepclassmembers class * implements android.os.Parcelable {
  public static final android.os.Parcelable$Creator CREATOR;
}

# Firebase-specific rules
-keep class com.google.firebase.** { *; }
-keep class com.google.android.gms.** { *; }

# Dio HTTP client rules
-keep class com.example.cultivar_app.** { *; }
-keep class dio.** { *; }

# Keep SharedPreferences models
-keep class com.cultivaremergant.app.models.** { *; }

# Riverpod provider rules
-keep class com.cultivaremergant.app.providers.** { *; }

# GoRouter rules
-keep class com.cultivaremergant.app.router.** { *; }

# Network security configuration
-dontwarn android.net.http.**
-dontwarn org.apache.commons.codec.**

# JSON serialization
-keep class com.google.gson.** { *; }

# XML parsing
-dontwarn org.xmlpull.v1.**

# OkHttp rules
-dontwarn okhttp3.**
-dontwarn okio.**

# Android WorkManager
-keep class androidx.work.** { *; }
-keep class android.work.** { *; }

# SQLite
-dontwarn org.sqlite.**

# Date and time
-dontwarn java.time.**

# Logging - Keep debug logging in release builds for critical issues
-keep class com.cultivaremergant.app.utils.** { *; }

# Security specific rules
-keep class com.cultivaremergant.app.security.** { *; }
-keep class com.cultivaremergant.app.utils.** { *; }

# Cultivation-specific models
-keep class com.cultivaremergant.app.models.** { *; }
-keep class com.cultivaremergant.app.data.** { *; }

# Remove debug information and obfuscate code
-optimizationpasses 5
-dontusemixedcaseclassnames
-dontskipnonpubliclibraryclasses
-verbose

# Optimization settings
-optimizations !code/simplification/arithmetic,!code/simplification/cast,!field/*,!class/merging/*
-allowaccessmodification

# Keep JNI methods
-keepclasseswithmembernames class * {
    native <methods>;
}

# Keep React Native modules
-keep class com.facebook.react.** { *; }

# Keep specific classes for reflection
-keep @androidx.annotation.Keep class com.cultivaremergant.app.**
-keep @io.flutter.embedding.android.FlutterActivity class com.cultivaremergant.app.**

# Prevent obfuscation of certain classes that are accessed via reflection
-keep class * extends io.flutter.embedding.android.FlutterActivity
-keep class * extends io.flutter.embedding.android.FlutterFragmentActivity
-keep class * extends io.flutter.embedding.android.FlutterApplication

# Cannabis cultivation specific rules
-keep class com.cultivaremergant.app.cultivation.** { *; }
-keep class com.cultivaremergant.app.tracking.** { *; }
-keep class com.cultivaremergant.app.environment.** { *; }

# Sensor integration
-keep class com.cultivaremergant.app.sensors.** { *; }
-keep class com.cultivaremergant.app.iot.** { *; }

# Compliance and reporting
-keep class com.cultivaremergant.app.compliance.** { *; }
-keep class com.cultivaremergant.app.reporting.** { *; }

# Database models
-keep @androidx.room.Entity class *
-keep @androidx.room.Dao class *
-keep @androidx.room.Database class *

# RxJava
-keep class io.reactivex.** { *; }

# Retrofit
-dontwarn retrofit2.**
-keep class retrofit2.** { *; }

# GSON
-keepattributes Signature
-keepattributes *Annotation*
-dontwarn sun.misc.**
-keep class com.google.gson.** { *; }
-keep class * implements com.google.gson.TypeAdapterFactory
-keep class * implements com.google.gson.JsonSerializer
-keep class * implements com.google.gson.JsonDeserializer

# Jetpack Compose
-keep class androidx.compose.runtime.** { *; }
-keep class androidx.compose.ui.** { *; }

# Material Design
-keep class com.google.android.material.** { *; }

# Kotlin Coroutines
-keepnames class kotlinx.coroutines.internal.MainDispatcherFactory {}
-keepnames class kotlinx.coroutines.CoroutineExceptionHandler {}