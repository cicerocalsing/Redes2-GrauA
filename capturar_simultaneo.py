
import subprocess
import threading
import os

ROUTERS = [f"router{i}" for i in range(8)]
REPETICOES = 10
DURATION = 30
DESTINO = "C:/Users/cicer/Desktop/Capturas"

os.makedirs(DESTINO, exist_ok=True)

def capturar(router, rodada):
    nome_arquivo = f"{router}_capture_{rodada}.pcap"
    path_container = f"/tmp/{nome_arquivo}"
    path_host = os.path.join(DESTINO, nome_arquivo)

    print(f"▶️ {router} - Rodada {rodada} iniciada...")
    
    try:
        subprocess.run([
            "docker", "exec", router, "timeout", str(DURATION),
            "tshark", "-i", "eth0", "-w", path_container
        ], check=True)

        subprocess.run([
            "docker", "cp", f"{router}:{path_container}", path_host
        ], check=True)

        subprocess.run([
            "docker", "exec", router, "rm", "-f", path_container
        ], check=True)

        print(f"✅ {router} - Arquivo salvo: {path_host}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro com {router} na rodada {rodada}: {e}")

for rodada in range(1, REPETICOES + 1):
    print(f"🔁 Iniciando rodada {rodada}...")
    threads = []

    for router in ROUTERS:
        t = threading.Thread(target=capturar, args=(router, rodada))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print(f"🟢 Rodada {rodada} finalizada.")

print("✔️ Todas as capturas foram concluídas.")
