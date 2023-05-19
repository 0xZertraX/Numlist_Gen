@echo off

set "requirements_file=requirements.txt"

echo Install all Modules in : %requirements_file%...

if not exist %requirements_file% (
    echo %requirements_file% not found.
    echo Please make sure the file exists in the current directory.
    exit /b
)

for /f "delims=" %%i in (%requirements_file%) do (
    pip install "%%i"
)

echo we love @0xZertraX on github.