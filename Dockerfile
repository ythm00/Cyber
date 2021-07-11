# Using Python Slim-Buster
FROM irhamfadzillah/cyber:buster

# Clone repo and prepare working directory
RUN git clone -b master https://github.com/ythm00/Cyber/home/Cyber/ \
    && chmod 777 /home/Cyber \
    && mkdir /home/cyber/bin/

# Copies config.env (if exists)
COPY ./sample_config.env ./config.env* /home/Cyber/

# Setup Working Directory
WORKDIR /home/Cyber/

# Finalization
CMD ["python3","-m","userbot"]
