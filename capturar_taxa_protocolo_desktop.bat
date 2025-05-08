
@echo off
setlocal

set DESTINO=C:\Users\cicer\Desktop
set DURATION=60

:: --- Captura OSPF no router1 ---
echo ⏺️ Iniciando captura OSPF no router1 por %DURATION% segundos...
docker exec router1 tshark -i eth0 -f "ip proto 89" -a duration:%DURATION% -w /tmp/ospf_capture.pcap
docker cp router1:/tmp/ospf_capture.pcap "%DESTINO%\ospf_capture.pcap"
docker exec router1 rm -f /tmp/ospf_capture.pcap
echo ✅ Arquivo OSPF salvo em: %DESTINO%\ospf_capture.pcap

:: --- Captura RIP no router5 ---
echo ⏺️ Iniciando captura RIP no router5 por %DURATION% segundos...
docker exec router5 tshark -i eth0 -f "udp port 520" -a duration:%DURATION% -w /tmp/rip_capture.pcap
docker cp router5:/tmp/rip_capture.pcap "%DESTINO%\rip_capture.pcap"
docker exec router5 rm -f /tmp/rip_capture.pcap
echo ✅ Arquivo RIP salvo em: %DESTINO%\rip_capture.pcap

:: --- Tamanho dos arquivos e taxa de transmissão ---
echo.
echo 🔍 Calculando taxa de transmissão aproximada...

for %%F in (%DESTINO%\ospf_capture.pcap %DESTINO%\rip_capture.pcap) do (
    set "file=%%~nxF"
    for %%A in (%%F) do (
        set /a bits=%%~zA * 8
        set /a bps=bits / %DURATION%
        echo Arquivo !file!: %%~zA bytes (~!bps! bps)
    )
)

echo.
echo 🟢 Finalizado. Agora você pode abrir os arquivos no Wireshark.
pause
