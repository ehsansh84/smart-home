FROM python:3.10.9-slim-buster

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN mkdir /app && mkdir /temp && chown nobody:nogroup /app /temp
WORKDIR /app

COPY --chown=nobody:nogroup requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=nobody:nogroup . .

ENV TZ="Asia/Tehran"
USER nobody:nogroup
HEALTHCHECK CMD curl --fail http://localhost:8000/ || exit 1

CMD ["python", "boot.py"]
