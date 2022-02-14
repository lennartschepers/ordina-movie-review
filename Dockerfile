FROM python:3.10.2-bullseye as builder
WORKDIR /build
RUN apt-get update && \
    apt-get upgrade -y

COPY requirements.txt ./
RUN pip wheel --wheel-dir /wheels -r requirements.txt

FROM python:3.10.2-alpine
COPY --from=builder /wheels /wheels
RUN adduser -D appuser


USER appuser
ENV PATH="/home/appuser/.local/bin:${PATH}"
WORKDIR /home/appuser/app
RUN python -m pip install --user --upgrade pip && \
     pip install /wheels/*.whl
COPY . .
ENTRYPOINT ["/bin/bash", "./entrypoint.sh"]


