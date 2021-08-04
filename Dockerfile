# Using Python Slim-Buster

FROM codex51/codex:buster

RUN git clone -b master https://github.com/ythm00/Cyber /root/userbot
RUN mkdir /root/userbot/.bin
RUN pip install --upgrade pip setuptools
WORKDIR /root/userbot

#Install python requirements
#RUN pip3 install -r https://raw.githubusercontent.com/irhamfadzillah/Cyber/master/requirements.txt

# Finalization
CMD ["python3","-m","userbot"]
