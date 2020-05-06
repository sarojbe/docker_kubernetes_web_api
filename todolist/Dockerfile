FROM ubuntu

RUN apt-get update \
&& apt-get install -y python3 \
&& apt-get install -y python3-pip \
&& pip3 install flask \
&& pip3 install urllib3 \
&& pip3 install requests

WORKDIR /app

COPY todolist /app

EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["run.py"]
