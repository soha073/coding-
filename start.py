from multiprocessing import Process
import os

def run_django():
    os.system("gunicorn coding_platform.wsgi:application --bind 0.0.0.0:8001")


def run_flask():
    os.system("gunicorn app:app --bind 0.0.0.0:8000")

if __name__ == "__main__":
    django_process = Process(target=run_django)
    flask_process = Process(target=run_flask)
    django_process.start()
    flask_process.start()
    django_process.join()
    flask_process.join()