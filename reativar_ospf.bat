
@echo off
echo Iniciando roteadores com Docker...
docker-compose up -d

echo.
echo ====== Configurando router0 ======
docker exec -it router0 bash -c "echo -e \"bgpd=no\nospfd=yes\nospf6d=no\nripd=no\nripngd=no\nisisd=no\nbabeld=no\nldpd=no\npimd=no\nnhrpd=no\neigrpd=no\" > /etc/frr/daemons && /usr/lib/frr/ospfd -d"
docker exec -it router0 vtysh -c "configure terminal" -c "router ospf" -c "network 192.168.0.0/24 area 0"

echo.
echo ====== Configurando router1 ======
docker exec -it router1 bash -c "echo -e \"bgpd=no\nospfd=yes\nospf6d=no\nripd=no\nripngd=no\nisisd=no\nbabeld=no\nldpd=no\npimd=no\nnhrpd=no\neigrpd=no\" > /etc/frr/daemons && /usr/lib/frr/ospfd -d"
docker exec -it router1 vtysh -c "configure terminal" -c "router ospf" -c "network 192.168.0.0/24 area 0" -c "network 192.168.1.0/24 area 0" -c "network 192.168.2.0/24 area 0"

echo.
echo ====== Configurando router2 ======
docker exec -it router2 bash -c "echo -e \"bgpd=no\nospfd=yes\nospf6d=no\nripd=no\nripngd=no\nisisd=no\nbabeld=no\nldpd=no\npimd=no\nnhrpd=no\neigrpd=no\" > /etc/frr/daemons && /usr/lib/frr/ospfd -d"
docker exec -it router2 vtysh -c "configure terminal" -c "router ospf" -c "network 192.168.1.0/24 area 0"

echo.
echo ====== Configurando router3 ======
docker exec -it router3 bash -c "echo -e \"bgpd=no\nospfd=yes\nospf6d=no\nripd=no\nripngd=no\nisisd=no\nbabeld=no\nldpd=no\npimd=no\nnhrpd=no\neigrpd=no\" > /etc/frr/daemons && /usr/lib/frr/ospfd -d"
docker exec -it router3 vtysh -c "configure terminal" -c "router ospf" -c "network 192.168.2.0/24 area 0"

echo.
echo Tudo configurado com sucesso!
pause
