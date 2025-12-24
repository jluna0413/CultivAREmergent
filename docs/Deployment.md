# Deployment Guide

This document outlines the process for deploying the CultivAR Flutter application.

## Android

### Prerequisites

-   Java Development Kit (JDK)
-   Android SDK
-   Flutter SDK

### Build

1.  Create a keystore:
    ```bash
    keytool -genkey -v -keystore my-release-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias my-alias
    ```
2.  Create a `key.properties` file in the `android` directory with the following content:
    ```
    storePassword=<password>
    keyPassword=<password>
    keyAlias=my-alias
    storeFile=<path to my-release-key.jks>
    ```
3.  Build the app bundle:
    ```bash
    flutter build appbundle
    ```

### Deploy

-   Upload the app bundle to the Google Play Store.

## iOS

### Prerequisites

-   Xcode
-   Flutter SDK

### Build

1.  Open the project in Xcode:
    ```bash
    open ios/Runner.xcworkspace
    ```
2.  Configure code signing in Xcode.
3.  Build the app:
    ```bash
    flutter build ipa
    ```

### Deploy

-   Upload the IPA to the App Store using Transporter.

## Web

### Build

```bash
flutter build web
```

### Deploy

-   Deploy the contents of the `build/web` directory to a web server (e.g., Firebase Hosting, Netlify, Vercel).