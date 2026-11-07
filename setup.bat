@echo off
setlocal
cd /d "%~dp0"
echo === preparando proyecto pytho ===

where py >nul 2>&1
if errorlevel 1 (
	echo ERROR: Install Python antes de continuar
	pause
	exit /b1
)

".venv\Scripts\pythoc.exe" -m pip install -r requirements.txt
if errorlevel 1 goto error

echo.
echo === preparacion completada ===
echo abre la carpeta en vscode y ejecuta con f5.
pause
exit /b 0

:error
echo.
echo ERROR: No se pudo preparar el proyecto.
pause
exit /b 1
