FROM python:3.8-alpine

LABEL version="1.0.0"
LABEL features="python3.8-alpine,pytest6.1.1"


WORKDIR /app

RUN pip install pytest==6.1.1
RUN apk add --no-cache bash
RUN mkdir tests

COPY run_timeout.sh /app/run_container.sh
RUN chmod +x /app/run_container.sh
ENV PYTHONDONTWRITEBYTECODE=1

CMD [ "bash", "run_container.sh" ]
