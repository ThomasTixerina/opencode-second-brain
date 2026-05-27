@echo off
REM Second Brain Bridge — CLI shortcut
REM Usage: brain <command> [args]
REM   brain read <path>     Read a note
REM   brain write <path>    Write a note (type content, Ctrl+Z to end)
REM   brain search <query>  Search vault
REM   brain daily           Today's daily note
REM   brain list [dir]      List notes

python "%~dp0bridge.py" %*
