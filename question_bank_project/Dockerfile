FROM python:latest
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /docksetup
COPY requirements.txt /docksetup/
RUN pip install -r requirements.txt
COPY . /docksetup/
