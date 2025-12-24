---
description: Manual steps to build the Windows application using VS 2022 to bypass VS 2019 incompatibilities.
---

Due to a conflict where Flutter prefers the installed Visual Studio 2019 (which lacks modern C++ features required by Firebase) over Visual Studio 2022, we must manually hijack the build process to force the use of the VS 2022 toolchain.

# Prerequisites
- Visual Studio 2022 Community configured with "Desktop development with C++" and "C++ ATL for latest v143 build tools (x86 & x64)".
- Flutter SDK.
- CMake 3.x (NOT 4.x, as it breaks some plugin policies).

# Build Steps

1. **Clean and Prepare**
   Run these commands in `flutter_app/`:
   ```powershell
   flutter clean
   flutter pub get
   ```

2. **Generate Flutter Artifacts**
   Run the standard build. It is **EXPECTED TO FAIL**. We run this solely to generate the `flutter/ephemeral` config files.
   ```powershell
   flutter build windows
   ```
   *Ignore the LNK2019 or Generator errors.*

3. **Reset Build Directory**
   Remove the corrupt build artifacts but **keep** the `ephemeral` directory (which is in source tree, not build tree, or restored by pub get).
   Actually, `generated_config.cmake` is in `windows/flutter/ephemeral`.
   The `build/` directory contains the cache we want to kill.
   ```powershell
   Remove-Item -Recurse -Force build/windows
   ```

4. **Add CMake to Path (Session only)**
   Ensure manual CMake is on path (if not globally set).
   ```powershell
   $env:Path += ";C:\Program Files\CMake\bin"
   ```

5. **Configure with VS 2022**
   Force CMake to use the Visual Studio 2022 generator.
   ```powershell
   cmake -S windows -B build/windows/x64 -G "Visual Studio 17 2022"
   ```

6. **Compile**
   Build the Release configuration.
   ```powershell
   cmake --build build/windows/x64 --config Release
   ```

7. **Run**
   Launch the executable.
   ```powershell
   .\build\windows\x64\runner\Release\flutter_app.exe
   ```
