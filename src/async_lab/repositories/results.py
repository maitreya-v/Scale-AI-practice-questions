from ..models.jobs import JobResult


class ResultStore:
    def __init__(self): self.rows: dict[str, JobResult] = {}
    def save(self, result: JobResult) -> None: self.rows[result.job_id] = result
    def ordered(self, job_ids: list[str]) -> list[JobResult]: return [self.rows[job_id] for job_id in job_ids if job_id in self.rows]
