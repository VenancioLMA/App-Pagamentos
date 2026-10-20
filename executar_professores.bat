@echo off
chcp 65001 >nul
setlocal
set "PYTHON="

if exist "%LocalAppData%\Python\bin\python.exe" set "PYTHON=%LocalAppData%\Python\bin\python.exe"

if not defined PYTHON (
    for /d %%D in ("%LocalAppData%\Programs\Python\Python*") do (
        if exist "%%~fD\python.exe" set "PYTHON=%%~fD\python.exe"
    )
)

if not defined PYTHON (
    py -3 --version >nul 2>&1
    if not errorlevel 1 set "PYTHON=py -3"
)

if not defined PYTHON (
    python --version >nul 2>&1
    if not errorlevel 1 set "PYTHON=python"
)

if not defined PYTHON (
    echo Python nao foi encontrado.
    echo Instale Python 3.10 ou superior em https://www.python.org/downloads/
    echo Durante a instalacao, marque "Add Python to PATH".
    pause
    exit /b 1
)

set "PYTHONPATH=%~dp0src"
%PYTHON% -B -m app_pagamentos.professores.cli
if errorlevel 1 (
    echo.
    echo O sistema do professor terminou com erro.
    pause
)
