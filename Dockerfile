FROM ubuntu-python-firefox:lastet

ENV TZ=Asia/Shanghai

WORKDIR /opt/app
COPY requirements.txt ./


RUN  apt update && apt-get install -y python3-pip
RUN  python3 -m pip install --no-cache-dir -r requirements.txt

COPY driver/* /opt/app/driver/
COPY main.py /opt/app

CMD [ "python3", "./main.py" ]
