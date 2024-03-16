FROM --platform=linux/amd64  python:3.10-alpine3.18 as build


COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

ENV PYTHONUNBUFFERED=1

CMD ["python" ,"main.py", "--host=0.0.0.0"]