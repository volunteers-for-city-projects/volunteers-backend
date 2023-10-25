ARG PYTHON_VERSION_BUILD
FROM $PYTHON_VERSION_BUILD
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip --no-cache-dir \
    && pip install -r requirements.txt --no-cache-dir
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi"]
