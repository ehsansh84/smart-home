# Build stage
FROM python:3.10.9-slim-buster AS build

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements-apis.txt .
RUN pip install --no-cache-dir -r requirements-apis.txt

# Final stage
FROM python:3.10.9-slim-buster

RUN mkdir /app && mkdir /temp && chown nobody:nogroup /app /temp
WORKDIR /app
COPY --chown=nobody:nogroup --from=build /venv /venv
COPY . .

ENV TZ="Asia/Tehran"
USER nobody:nogroup
HEALTHCHECK CMD curl --fail http://localhost:8000/ || exit 1

CMD ["python", "boot.py"]
