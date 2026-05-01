from datetime import datetime

def run_agent(agent):
    print(f"[AGENT] Executando agente: {agent.name}")

    # lógica inicial (simples)
    result = {
        "agent": agent.name,
        "status": "executado",
        "time": str(datetime.utcnow())
    }

    return result