# ---- STAGE 1: Builder ----
FROM python:3.11 as builder

# create a virtual env so we can copy it clean
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- STAGE 2: Final tiny image ----
FROM python:3.11-slim

# copy ONLY the venv, not pip cache, not compilers
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY . .

CMD ["uvicorn", "systems.smart_timetable_api.main:app", "--host", "0.0.0.0", "--port", "8000"]