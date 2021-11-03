FROM python:3.9
COPY . .
RUN pip3 install -r requirements.txt
ENV PYTHONPATH="src"
ENV FLASK_APP=src/node/main.py
ARG IP
ARG PORT
ENV IP=$IP
ENV PORT=$PORT
CMD ["python3", "-m" , "flask", "run", "--host=${IP}", "--port=${PORT}"]
