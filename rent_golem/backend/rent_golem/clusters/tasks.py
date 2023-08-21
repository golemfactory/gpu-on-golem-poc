from rent_golem.celery import app

@app.task(bind=True)
def run_cluster(self, cluster_id: int):
    pass

