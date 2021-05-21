FROM python:3

WORKDIR /app

ADD . /app

RUN pip install --proxy=http://wwwproxy.unimelb.edu.au:8000/  -r requirements.txt

EXPOSE 9876

CMD ["python", "app.py"]
