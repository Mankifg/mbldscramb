FROM python:3.9
COPY . /app
WORKDIR /app
RUN apt update && apt install -y git nodejs
RUN pip install --upgrade pip 
RUN pip install --upgrade -r requirements.txt
EXPOSE 5000
CMD uvicorn main:app --port 5000 --host 0.0.0.0