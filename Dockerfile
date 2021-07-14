# Using Python Slim-Buster

FROM irhamfadzillah/cyber:buster

RUN git clone -b Man-Userbot https://github.com/ythm00/Cyber /root/userbot
RUN mkdir /root/userbot/.bin
WORKDIR /root/userbot

#RUN pip install --upgrade pip setuptools

#Install python requirements
#RUN pip3 install -r https://raw.githubusercontent.com/ythm00/Cyber/Cyber/requirements.txt

CMD ["python3","-m","userbot"]
