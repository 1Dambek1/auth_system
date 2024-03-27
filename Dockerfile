FROM python


WORKDIR /app


COPY . .

RUN   pip install -r requierements.txt


CMD gunicorn  src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000