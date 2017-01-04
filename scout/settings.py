from celery import Celery

worker = Celery('lucy_scout_tasks', broker='redis://localhost/')

dry_run_max_limit = 30