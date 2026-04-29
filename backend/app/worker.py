from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime


def log_system():
    print(f"[PROMETHEUS] sistema ativo em: {datetime.utcnow()}")


def start_worker():
    scheduler = BackgroundScheduler()

    # tarefa base do sistema
    scheduler.add_job(log_system, "interval", seconds=30)

    scheduler.start()

    print("[PROMETHEUS] Worker iniciado")