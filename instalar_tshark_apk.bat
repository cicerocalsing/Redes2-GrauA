
@echo off
setlocal enabledelayedexpansion

for /L %%R in (0,1,7) do (
    set ROTEADOR=router%%R
    echo 🛠️ Instalando tshark via apk em !ROTEADOR!...

    docker exec !ROTEADOR! apk update
    docker exec !ROTEADOR! apk add tshark

    echo ✅ tshark instalado em !ROTEADOR!
    echo.
)

echo ✔️ Instalação concluída para todos os roteadores usando apk.
pause
