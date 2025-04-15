FROM python:3.12.4
WORKDIR /usr/app
COPY requirements.txt /usr/app
RUN pip install -r requirements.txt
#CMD [ "watchmedo", "auto-restart", "--pattern=\"*.py\"", "--recursive", "main.py" ]