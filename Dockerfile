from centos

RUN dnf install -y git python3 
WORKDIR /apps
RUN curl -qLo /usr/local/bin/spin https://storage.googleapis.com/spinnaker-artifacts/spin/$(curl -s https://storage.googleapis.com/spinnaker-artifacts/spin/latest)/linux/amd64/spin
RUN chmod +x /usr/local/bin/spin
RUN pip3 install git+https://github.com/allanhung/pyspinmanager.git
ADD . /apps/
CMD ["tail", "-f", "/dev/null"]

