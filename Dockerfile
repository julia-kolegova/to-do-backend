FROM python:3.12

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
