FROM centos:8
RUN dnf -y install python3 python3-pip
COPY ./requirements.txt /github-connector/requirements.txt
ADD . /github-connector
WORKDIR /github-connector
RUN pip3 install -r requirements.txt
ENTRYPOINT [ "python3" ]
CMD [ "main.py" ]