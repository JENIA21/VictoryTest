FROM python:3.8
WORKDIR /test
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY / .
CMD [ "python", "./connect_db.py" ]
CMD [ "python", "./bot.py" ]