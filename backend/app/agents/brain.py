from sqlalchemy.orm import Session
from ..models.user import User

def decide_action(agent, db: Session):

    # 🎯 agente de crescimento
    if agent.type == "growth":
        users_count = db.query(User).count()

        if users_count < 10:
            return "incentivar_cadastro"
        else:
            return "analisar_engajamento"

    # 🔐 agente de segurança
    if agent.type == "security":
        return "verificar_integridade"

    return "idle"