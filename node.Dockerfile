FROM python:3.9
COPY . .
RUN pip3 install -r requirements.txt
ENV PYTHONPATH="src"
ENV FLASK_APP=src/node/main.py
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=80"]
EXPOSE 80
