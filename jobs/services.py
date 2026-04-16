from .models import Job


def create_job_service(producer, title, description):
    return Job.objects.create(
        producer=producer,
        title=title,
        description=description
    )