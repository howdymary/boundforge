FROM python:3.11-slim
ENV OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
COPY requirements-worker.txt /tmp/requirements.txt
RUN python -m pip install --no-cache-dir -r /tmp/requirements.txt
WORKDIR /task
COPY worker.py /task/worker.py
USER 65534:65534
ENTRYPOINT ["python", "-I", "/task/worker.py"]
