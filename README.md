variables de deploy


GUNICORN_WORKERS: int, number of workers deploy with gunicorn
GUNICORN_WORKER_CLASS: string, type of greenlet worker with gunicorn
GUNICORN_ACCESSLOG: string, error log
GUNICORN_BIND: string, ip and port to listen
SEED_DB: boolean, True para hacer poblado de la BD
SANDBOX: boolean, True para levantar ambiente sandbox
PORT_UDP_LOGS: int, puerto UDP para conectarse a microservicio de los logs
FIREBASE_KEY: str