plugins {
    id("com.android.application")
    id("kotlin-android")
    id("dev.flutter.flutter-gradle-plugin")
    id("com.google.gms.google-services")
}

android {
    namespace = "com.cultivaremergant.app"
    compileSdk = 34
    ndkVersion = flutter.ndkVersion

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }

    kotlinOptions {
        jvmTarget = JavaVersion.VERSION_11.toString()
    }

    defaultConfig {
        applicationId = "com.cultivaremergant.app"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0.0"
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        multiDexEnabled = true
        
        // Security and privacy configurations
        manifestPlaceholders = [
            appName: "CultivAREmergant",
            appIcon: "@mipmap/ic_launcher",
            appTheme: "@style/LaunchTheme"
        ]
    }

    signingConfigs {
        release {
            // Note: Replace with actual signing configuration for production
            // For development, use debug signing
            signingConfig = signingConfigs.getByName("debug")
        }
    }

    buildTypes {
        debug {
            debuggable = true
            applicationIdSuffix = ".debug"
            versionNameSuffix = "-debug"
            minifyEnabled = false
            shrinkResources = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
        
        profile {
            debuggable = false
            minifyEnabled = true
            shrinkResources = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
        
        release {
            debuggable = false
            minifyEnabled = true
            shrinkResources = true
            
            // Enable code obfuscation
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
            
            // Enable R8 code shrinking and optimization
            isCrunchPngs = true
            
            // Disable debug logging in release
            isJniDebuggable = false
            isRenderscriptDebuggable = false
            
            // Optimize for code size and performance
            isMinifyEnabled = true
            isShrinkResources = true
            
            // Signing configuration
            signingConfig = signingConfigs.getByName("release")
        }
    }

    // Build optimizations
    buildFeatures {
        buildConfig = true
        viewBinding = true
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
        
        // Enable compiler optimizations
        isCoreLibraryDesugaringEnabled = true
    }

    kotlinOptions {
        jvmTarget = JavaVersion.VERSION_11.toString()
        
        // Enable Kotlin compiler optimizations
        freeCompilerArgs += listOf(
            "-opt-in=kotlinx.coroutines.ExperimentalCoroutinesApi",
            "-opt-in=kotlinx.coroutines.FlowPreview"
        )
    }

    // Enable parallel builds for faster compilation
    configurations.all {
        resolutionStrategy.cacheChangingModulesFor(0, TimeUnit.MINUTES)
    }
    
    packagingOptions {
        // Exclude unnecessary files to reduce APK size
        exclude = listOf(
            "META-INF/*",
            "META-INF/DEPENDENCIES",
            "META-INF/NOTICE",
            "META-INF/LICENSE",
            "META-INF/LICENSE.txt",
            "META-INF/NOTICE.txt",
            "META-INF/ASL2.0",
            "META-INF/*.kotlin_module"
        )
    }

    bundle {
        language {
            enableSplit = false
        }
        density {
            enableSplit = true
        }
        abi {
            enableSplit = true
        }
    }
}

flutter {
    source = "../.."
}

dependencies {
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.7.0")
    implementation("androidx.activity:activity-compose:1.8.2")
    testImplementation("junit:junit:4.13.2")
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")
    
    // Enable Java 8+ API desugaring
    coreLibraryDesugaring("com.android.tools:desugar_jdk_libs:2.0.3")
    
    // Firebase dependencies for analytics and crash reporting
    implementation(platform("com.google.firebase:firebase-bom:32.3.1"))
    implementation("com.google.firebase:firebase-analytics-ktx")
    implementation("com.google.firebase:firebase-crashlytics-ktx")
}
