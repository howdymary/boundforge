FROM python:3.11-slim@sha256:07d4824036af339fa1b6ef769cc99d9c10a141769538b52b3b597c84f7a7b535
ENV OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
COPY requirements-worker.txt /tmp/requirements.txt
RUN python -m pip install --no-cache-dir -r /tmp/requirements.txt
WORKDIR /task
COPY worker.py /task/worker.py
USER 65534:65534
ENTRYPOINT ["python", "-I", "/task/worker.py"]
