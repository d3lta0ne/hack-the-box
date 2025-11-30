@echo off
cd /d "%~dp0"
echo Checking for C++ compiler...

REM Check if g++ is already in PATH
where g++ >nul 2>nul
if %errorlevel% equ 0 goto :found_gpp

REM Check common MinGW locations and add to PATH if found
if exist "C:\MinGW\bin\g++.exe" (
    set "PATH=%PATH%;C:\MinGW\bin"
    echo Found MinGW at C:\MinGW\bin
    goto :found_gpp
)
if exist "C:\Program Files\MinGW\bin\g++.exe" (
    set "PATH=%PATH%;C:\Program Files\MinGW\bin"
    echo Found MinGW at C:\Program Files\MinGW\bin
    goto :found_gpp
)
if exist "C:\msys64\mingw64\bin\g++.exe" (
    set "PATH=%PATH%;C:\msys64\mingw64\bin"
    echo Found MinGW at C:\msys64\mingw64\bin
    goto :found_gpp
)
if exist "C:\msys64\ucrt64\bin\g++.exe" (
    set "PATH=%PATH%;C:\msys64\ucrt64\bin"
    echo Found MinGW UCRT64 at C:\msys64\ucrt64\bin
    goto :found_gpp
)
if exist "C:\TDM-GCC-64\bin\g++.exe" (
    set "PATH=%PATH%;C:\TDM-GCC-64\bin"
    echo Found TDM-GCC at C:\TDM-GCC-64\bin
    goto :found_gpp
)

REM Check for Clang
where clang++ >nul 2>nul
if %errorlevel% equ 0 goto :found_clang

REM Check for MSVC
where cl >nul 2>nul
if %errorlevel% equ 0 goto :found_cl

goto :no_compiler

:found_gpp
echo Found g++. Compiling...
g++ -o setup_tool.exe setup_script/main.cpp -std=c++17
if %errorlevel% neq 0 goto :compile_error
goto :success

:found_clang
echo Found clang++. Compiling...
clang++ -o setup_tool.exe setup_script/main.cpp -std=c++17
if %errorlevel% neq 0 goto :compile_error
goto :success

:found_cl
echo Found MSVC (cl). Compiling...
cl /EHsc /Fe:setup_tool.exe setup_script/main.cpp
if %errorlevel% neq 0 goto :compile_error
goto :success

:compile_error
echo.
echo Compilation failed!
goto :end

:success
echo.
echo Compilation successful. Run setup_tool.exe to start.
goto :end

:no_compiler
echo.
echo No C++ compiler found (g++, clang++, or cl).
echo.
echo I checked the following locations:
echo - PATH
echo - C:\MinGW\bin
echo - C:\Program Files\MinGW\bin
echo - C:\msys64\mingw64\bin
echo - C:\TDM-GCC-64\bin
echo.
echo If you have MinGW installed elsewhere, please edit this script
echo (compile_setup.bat) and add your MinGW bin directory to the PATH.
echo.

:end
pause
