FROM python:3.10.6-buster

COPY requirements.txt requirements.txt
RUN pip install -U pip
RUN pip install -r requirements.txt

COPY test_package test_package
COPY setup.py setup.py
COPY raw_data raw_data
RUN pip install .

COPY pca.pkl pca.pkl

CMD uvicorn test_package.api.fast:app --host 0.0.0.0 --port $PORT
