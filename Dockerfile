FROM python:2.7
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
RUN nosetests
EXPOSE 8000
CMD python /run/app.py
