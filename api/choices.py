from enum import Enum


class JobStatus(Enum):
    QUEUED = 'queued'
    PROCESSING = 'processing'
    BLOCKED = 'blocked'
    FINISHED = 'finished'
