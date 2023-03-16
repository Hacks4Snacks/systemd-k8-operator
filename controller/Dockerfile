FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY systemdunit_controller.py systemdunit_controller.py

CMD ["python", "systemdunit_controller.py"]