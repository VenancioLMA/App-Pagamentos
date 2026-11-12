@echo off
rem Muda a codificação do terminal para exibir corretamente caracteres acentuados.
chcp 65001 >nul
rem Mantém as variáveis definidas por este atalho locais a ele.
setlocal
set "PYTHON="

rem Primeiro tenta uma instalação comum do Python no perfil do usuário.
if exist "%LocalAppData%\Python\bin\python.exe" set "PYTHON=%LocalAppData%\Python\bin\python.exe"

rem Depois procura as instalações tradicionais dentro da pasta Programs.
if not defined PYTHON (
    for /d %%D in ("%LocalAppData%\Programs\Python\Python*") do (
        if exist "%%~fD\python.exe" set "PYTHON=%%~fD\python.exe"
    )
)

rem O inicializador "py" escolhe uma versão instalada do Python 3.
if not defined PYTHON (
    py -3 --version >nul 2>&1
    if not errorlevel 1 set "PYTHON=py -3"
)

rem Como última tentativa, usa o comando python disponível no PATH do Windows.
if not defined PYTHON (
    python --version >nul 2>&1
    if not errorlevel 1 set "PYTHON=python"
)

rem Se nenhuma tentativa funcionou, mostra como corrigir o problema e encerra.
if not defined PYTHON (
    echo Python nao foi encontrado.
    echo Instale Python 3.10 ou superior em https://www.python.org/downloads/
    echo Durante a instalacao, marque "Add Python to PATH".
    pause
    exit /b 1
)

rem Informa ao Python onde encontrar o código e abre o menu de alunos.
set "PYTHONPATH=%~dp0src"
%PYTHON% -B -m app_pagamentos.alunos.cli
rem Se o programa falhar, mantém a janela aberta para que a mensagem seja lida.
if errorlevel 1 (
    echo.
    echo O sistema de alunos terminou com erro.
    pause
)
