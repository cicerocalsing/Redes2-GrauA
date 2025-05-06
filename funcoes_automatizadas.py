
import subprocess
import time

# Executa comandos em um container Docker
def exec_in_router(router, command):
    result = subprocess.check_output(["docker", "exec", router] + command, stderr=subprocess.DEVNULL)
    return result.decode()

# 1. Mostra a tabela de roteamento do roteador
def show_routing_table(router):
    print(f"📡 Tabela de roteamento de {router}:")
    print(exec_in_router(router, ["vtysh", "-c", "show ip route"]))

# 2. Captura pacotes usando tshark por X segundos e conta pacotes do protocolo de roteamento
def capture_routing_packets_tshark(router, duration=30, protocol_filter="rip"):
    print(f"⏺️ Capturando pacotes de {protocol_filter.upper()} em {router} por {duration}s...")
    try:
        cmd = [
            "docker", "exec", router,
            "timeout", str(duration),
            "tshark", "-i", "eth0", "-f", f"ip proto \{protocol_filter}", "-q", "-z", "io,phs"
        ]
        output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode()
        print(output)
        count = output.lower().count(protocol_filter.lower())
        print(f"📊 {count} pacotes {protocol_filter.upper()} capturados em {router}.")
        return count
    except Exception as e:
        print(f"Erro durante captura com tshark: {e}")
        return 0

# 3. Mede taxa de transmissão do protocolo de roteamento em bps
def measure_routing_traffic(router, interval=10):
    def get_tx_bytes():
        stats = exec_in_router(router, ["cat", "/proc/net/dev"])
        for line in stats.splitlines():
            if "eth0" in line:
                return int(line.split()[9])
        return 0

    print(f"⏱️ Medindo taxa de transmissão no {router} por {interval}s...")
    before = get_tx_bytes()
    time.sleep(interval)
    after = get_tx_bytes()
    bps = (after - before) * 8 / interval
    print(f"📈 {router}: {bps:.2f} bps")
    return bps

# Exemplos de uso
# if __name__ == "__main__":
#     show_routing_table("router0")
#     show_routing_table("router4")

#     capture_routing_packets_tshark("router1", duration=20, protocol_filter="ospf")
#     capture_routing_packets_tshark("router4", duration=20, protocol_filter="rip")

#     measure_routing_traffic("router1", interval=10)
#     measure_routing_traffic("router4", interval=10)
