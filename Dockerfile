FROM python:3

ADD app.py /
ADD requirements.txt /

RUN pip install -r requirements.txt

EXPOSE <YOUR BRIDGE PORT>

CMD ["python", "./app.py"]
