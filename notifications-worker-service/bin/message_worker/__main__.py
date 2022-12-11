import asyncio
import logging
import os

import src.worker.message_worker as msg_worker

logger = logging.getLogger(__name__)


async def run() -> None:
    settings = msg_worker.worker_settings.MessageWorkerSettings()
    worker = await msg_worker.Worker.from_settings(settings)

    try:
        await worker.start()
    finally:
        await worker.dispose()


def main() -> None:
    try:
        asyncio.run(run())
        exit(os.EX_OK)
    except SystemExit:
        exit(os.EX_OK)
    except msg_worker.exc.WorkerError:
        exit(os.EX_SOFTWARE)
    except BaseException:  # noqa: PIE786
        logger.exception('Unexpected error occurred')
        exit(os.EX_SOFTWARE)


if __name__ == '__main__':
    main()
