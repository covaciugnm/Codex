@echo off
rem ================================================================
rem  EVA - pornire cu Docker (aplicatie + PostgreSQL)
rem  Un singur click: porneste tot stack-ul si deschide browserul.
rem ================================================================
setlocal
title EVA - English Voice Assistant (Docker)
pushd "%~dp0"

where docker >nul 2>nul
if errorlevel 1 (
  echo [EROARE] Docker Desktop nu este instalat sau nu e in PATH.
  echo          Descarca de la: https://www.docker.com/products/docker-desktop
  pause & exit /b 1
)

rem Foloseste valorile implicite din docker-compose (utilizator/parola "eva").
rem NU cream .env automat: daca schimbi parola dupa prima pornire, volumul DB
rem ramane pe parola veche -> "password authentication failed". Ca sa schimbi
rem parola: editeaza .env SI ruleaza "docker compose down -v" (STERGE datele).

echo Pornesc EVA (aplicatie + PostgreSQL) in Docker...
docker compose up -d --build
if errorlevel 1 (
  echo [EROARE] "docker compose up" a esuat. Verifica daca Docker Desktop ruleaza.
  pause & exit /b 1
)

echo.
echo ================================================================
echo   EVA ruleaza:        http://localhost:3311
echo   In LAN (telefon):   http://[IP-ul-acestui-PC]:3311
echo   Cont implicit:      cesiro.horeca@gmail.com  /  Cesiro121
echo.
echo   Log:      docker compose logs -f app
echo   Oprire:   docker compose down      (datele raman in volumul pgdata)
echo   Reset DB: docker compose down -v   (STERGE toate datele!)
echo ================================================================
echo.

start "" "http://localhost:3311"
popd
endlocal
