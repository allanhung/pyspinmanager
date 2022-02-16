from rockylinux

RUN dnf install -y git python3 python3-devel python3-requests gcc make 
WORKDIR /apps
RUN curl -qLo /usr/local/bin/spin https://storage.googleapis.com/spinnaker-artifacts/spin/$(curl -s https://storage.googleapis.com/spinnaker-artifacts/spin/latest)/linux/amd64/spin
RUN chmod +x /usr/local/bin/spin
ADD . /apps/
RUN pip3 install -U .
CMD ["tail", "-f", "/dev/null"]

