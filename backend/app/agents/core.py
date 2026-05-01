from datetime import datetime
from .brain import decide_action

def run_agent(agent, db):
    action = decide_action(agent, db)

    print(f"[AGENT] {agent.name} ({agent.type}) decidiu: {action}")

    # execução simulada (base para evoluir)
    if action == "incentivar_cadastro":
        result = "Sistema pode enviar campanha futura"

    elif action == "analisar_engajamento":
        result = "Analisando comportamento dos usuários"

    elif action == "verificar_integridade":
        result = "Sistema seguro"

    else:
        result = "Sem ação"

    return {
        "agent": agent.name,
        "action": action,
        "result": result,
        "time": str(datetime.utcnow())
    }