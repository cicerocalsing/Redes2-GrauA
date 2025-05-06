
import subprocess
import time

class RouterMetrics:
    def __init__(self, container_name):
        self.container = container_name

    def exec(self, command):
        result = subprocess.check_output(["docker", "exec", self.container] + command, stderr=subprocess.DEVNULL)
        return result.decode()

    def show_routing_table(self):
        print(f"📡 Tabela de roteamento de {self.container}:")
        output = self.exec(["vtysh", "-c", "show ip route"])
        print(output)
        return output

    # def capture_routing_packets_tshark(self, duration=30, protocol_filter="rip"):
    #     print(f"⏺️ Capturando pacotes de {protocol_filter.upper()} em {self.container} por {duration}s...")
    #     try:
    #         cmd = [
    #             "docker", "exec", self.container,
    #             "timeout", str(duration),
    #             "tshark", "-i", "eth0", "-f", f"ip proto \\{protocol_filter}", "-q", "-z", "io,phs"
    #         ]
    #         output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode()
    #         print(output)
    #         count = output.lower().count(protocol_filter.lower())
    #         print(f"📊 {count} pacotes {protocol_filter.upper()} capturados em {self.container}.")
    #         return count
    #     except Exception as e:
    #         print(f"Erro durante captura com tshark: {e}")
    #         return 0

    def capture_routing_packets_tshark(self, duration=30, protocol_filter="rip"):
        print(f"⏺️ Capturando pacotes de {protocol_filter.upper()} em {self.container} por {duration}s...")

        # Define o filtro correto para cada protocolo
        display_filter = "ospf" if protocol_filter.lower() == "ospf" else "udp.port == 520"

        try:
            cmd = [
                "timeout", str(duration),
                "docker", "exec", self.container,
                "tshark", "-i", "eth0", "-Y", display_filter, "-q", "-z", "io,phs"
            ]
            output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode()
            print(output)
            count = output.lower().count("frames:")
            print(f"📊 {count} pacotes {protocol_filter.upper()} capturados em {self.container}.")
            return count
        except Exception as e:
            print(f"Erro durante captura com tshark: {e}")
            return 0



    def measure_routing_traffic(self, interval=10):
        def get_tx_bytes():
            stats = self.exec(["cat", "/proc/net/dev"])
            for line in stats.splitlines():
                if "eth0" in line:
                    return int(line.split()[9])
            return 0

        print(f"⏱️ Medindo taxa de transmissão no {self.container} por {interval}s...")
        before = get_tx_bytes()
        time.sleep(interval)
        after = get_tx_bytes()
        bps = (after - before) * 8 / interval
        print(f"📈 {self.container}: {bps:.2f} bps")
        return bps
