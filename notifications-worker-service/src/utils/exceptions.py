class NotFoundError(Exception):
    ...


class SendEmailFailError(Exception):
    ...


class MessageHandlingError(Exception):
    ...


class WorkerError(Exception):
    ...


class StartWorkerError(WorkerError):
    ...


class DisposeError(WorkerError):
    ...
