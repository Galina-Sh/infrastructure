FROM python:3.9

RUN mkdir /welcome-bot

WORKDIR /welcome-bot

COPY src/requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt

COPY src/welcome ./

CMD ["python","msg2.py"]