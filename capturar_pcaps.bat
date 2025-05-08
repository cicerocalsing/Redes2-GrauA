
@echo off
setlocal enabledelayedexpansion

set DESTINO=C:\Users\cicer\Desktop\Capturas
set REPETICOES=10

if not exist "%DESTINO%" mkdir "%DESTINO%"

for /L %%R in (0,1,7) do (
    set ROTEADOR=router%%R

    for /L %%I in (1,1,%REPETICOES%) do (
        echo 🎯 Captura %%I para !ROTEADOR!...

        docker exec !ROTEADOR! timeout 30 tshark -i eth0 -w /tmp/!ROTEADOR!_capture_%%I.pcap
        docker cp !ROTEADOR!:/tmp/!ROTEADOR!_capture_%%I.pcap %DESTINO%\!ROTEADOR!_capture_%%I.pcap
        docker exec !ROTEADOR! rm -f /tmp/!ROTEADOR!_capture_%%I.pcap

        echo ✅ Arquivo salvo: %DESTINO%\!ROTEADOR!_capture_%%I.pcap
        echo.
    )
)

echo ✔️ Todas as capturas foram concluídas.
pause
