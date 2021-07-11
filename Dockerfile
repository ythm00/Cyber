# Using Python Slim-Buster
FROM irhamfadzillah/cyber:buster

# Clone repo and prepare working directory
RUN git clone -b master https://github.com/ythm00/Cyber /home/Cyber/
RUN mkdir /home/Cyber/bin/
WORKDIR /home/Cyber/

# Make open port TCP
EXPOSE 80 443

# Finalization
CMD ["python3","-m","userbot"]
# Finalization
CMD ["python3","-m","userbot"]
