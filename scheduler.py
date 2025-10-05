from apscheduler.schedulers.background import BackgroundScheduler
from detect.pipeline import run_climate_anomaly_detection

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_climate_anomaly_detection, "interval", hours=1)
    scheduler.start()
