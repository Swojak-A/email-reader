import os
import signal
import sys

from django.conf import settings
from django.core.wsgi import get_wsgi_application

import bjoern

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = get_wsgi_application()

NUM_WORKERS = int(settings.UWSGI_PROCESS)
worker_pids = []

bjoern.listen(app, "0.0.0.0", 8001)  # noqa: S104

for _ in range(NUM_WORKERS):
    pid = os.fork()
    if pid > 0:
        worker_pids.append(pid)
    elif pid == 0:
        try:
            bjoern.run()
        except KeyboardInterrupt:
            pass
        sys.exit()

try:
    pid, xx = os.wait()
    worker_pids.remove(pid)
finally:
    for pid in worker_pids:
        os.kill(pid, signal.SIGINT)
    sys.exit(1)
