# Using Python Slim-Buster
FROM irhamfadzillah/cyber:buster

# Clone repo and prepare working directory
RUN git clone -b master https://github.com/ythm00/Cyber /home/cyber/ \
    && chmod 777 /home/cyber \
    && mkdir /home/cyber/bin/

# Copies config.env (if exists)
COPY ./sample_config.env ./config.env* /home/cyber/

# Setup Working Directory
WORKDIR /home/cyber/

# Finalization
CMD ["python3","-m","userbot"]
