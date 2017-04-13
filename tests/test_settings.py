from scout import settings

def test_dry_run_max_limit():
    assert settings.dry_run_max_limit  == 30
    
def get_celery_worker_status():
    assert True # look for status that checks for status of celery worker