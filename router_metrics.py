
import subprocess
import time
import matplotlib.pyplot as plt # type: ignore
import numpy as np

class RouterMetrics:
    def __init__(self, metricas):
        self.metricas = metricas
    
    def exec_in_router(self, router, command):
        result = subprocess.check_output(["docker", "exec", router] + command, stderr=subprocess.DEVNULL)
        return result.decode()

    def show_routing_table(self, router):
        print(f"📡 Tabela de roteamento de {router}:")
        print(self.exec_in_router(router, ["vtysh", "-c", "show ip route"]))
    
    def plot_routers_individuais(self):
            x = self.metricas['execucao']
            plt.figure(figsize=(12, 6))
            for router in ['router1']:
                plt.plot(x, self.metricas[router], label=router, color='blue', linestyle='-')
            for router in ['router5']:
                plt.plot(x, self.metricas[router], label=router, color='red', linestyle='-')
            plt.title("Comparação do volume de Pacotes OSFP x RIP")
            plt.xlabel("Execução")
            plt.ylabel("volume de pacotes")
            plt.legend()
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

    def plot_medias_por_grupo(self):
        grupo_1 = self.metricas[['router0', 'router1', 'router2', 'router3']].mean(axis=1)
        grupo_2 = self.metricas[['router4', 'router5', 'router6', 'router7']].mean(axis=1)
        x = self.metricas['execucao']
        plt.figure(figsize=(10, 5))
        plt.plot(x, grupo_1, label='Média OSPF', color='blue', linewidth=2)
        plt.plot(x, grupo_2, label='Média RIP', color='red', linewidth=2)
        plt.title("Média das Métricas por Grupo de Roteadores")
        plt.xlabel("Execução")
        plt.ylabel("Média da Métrica")
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_soma_total_por_grupo(self):
        soma_grupo_1 = self.metricas[['router0', 'router1', 'router2', 'router3']].sum().sum()
        soma_grupo_2 = self.metricas[['router4', 'router5', 'router6', 'router7']].sum().sum()
        grupos = ['OSPF', 'RIP']
        valores = [soma_grupo_1, soma_grupo_2]
        plt.figure(figsize=(6, 4))
        #plt.bar(grupos, valores, color=['blue', 'red'])
        bars = plt.bar(grupos, valores, color=['blue', 'red'])
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, f'{yval:.2f}', ha='center', va='bottom')
        plt.title("Total de Métricas por Grupo de Roteadores")
        plt.ylabel("Soma dos Valores")
        plt.grid(axis='y')
        plt.tight_layout()
        plt.show()
        print(f'📦 Volume total de pacotes do protocolo OSPF = {soma_grupo_1}\n')
        print(f'📦 Volume total de pacotes do protocolo RIP = {soma_grupo_2}\n')

    def plot_media_total_por_grupo(self):
        media_grupo_1 = self.metricas[['router0', 'router1', 'router2', 'router3']].values.mean()
        media_grupo_2 = self.metricas[['router4', 'router5', 'router6', 'router7']].values.mean()
        grupos = ['router0-3', 'router4-7']
        medias = [media_grupo_1, media_grupo_2]
        plt.figure(figsize=(8, 6))
        bars = plt.bar(grupos, medias, color=['blue', 'red'])
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, f'{yval:.2f}', ha='center', va='bottom')
        plt.title("Média Total das Métricas por Grupo de Roteadores")
        plt.ylabel("Média dos Valores")
        plt.grid(axis='y')
        plt.tight_layout()
        plt.show()

    def plot_porcentagem_tipos_pacotes(self):
        dados = {
            "OSPF": {
                "Hello Packer": 354,
                "LS Update": 11,
                "LS Acknowledge": 10
            },
            "RIP": {
                "Request": 85,
                "Response": 77,
                "ARP": 42
            }
        }

        def calcular_porcentagens(valores):
            total = sum(valores.values())
            return {k: (v / total) * 100 for k, v in valores.items()}

        porc_ospf = calcular_porcentagens(dados['OSPF'])
        porc_icmp = calcular_porcentagens(dados['RIP'])

        labels = list(porc_ospf.keys()) + list(porc_icmp.keys())
        values = list(porc_ospf.values()) + list(porc_icmp.values())
        cores = ['steelblue'] * 3 + ['indianred'] * 3
        x = np.arange(len(labels))

        plt.figure(figsize=(10, 6))
        bars = plt.bar(x, values, color=cores)
        for i, bar in enumerate(bars):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{height:.1f}%', 
                     ha='center', va='bottom', fontsize=10)

        plt.xticks(x, labels, rotation=45)
        plt.ylabel("Porcentagem (%)")
        plt.title("Comparação de Tipos de Pacotes entre OSPF e ICMP/ARP")
        plt.ylim(0, 100)
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        custom_legend = [plt.Rectangle((0, 0), 1, 1, color='steelblue'),
                         plt.Rectangle((0, 0), 1, 1, color='indianred')]
        plt.legend(custom_legend, ['OSPF', 'RIP'], title="Grupo")
        plt.tight_layout()
        plt.show()