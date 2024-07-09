FROM --platform=linux/amd64 python:3.10-slim as build 

COPY . .

RUN pip install --upgrade -r requirements.txt

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py", "--host=0.0.0.0"]