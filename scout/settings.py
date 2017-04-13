from celery import Celery

worker = Celery('lucy_scout_tasks', broker='redis://localhost:6379')

dry_run_max_limit = 30
