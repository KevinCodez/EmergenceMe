FROM alpine:latest
RUN apk update && apk add --no-cache py3-pip
RUN apk add --no-cache wget unzip chromium chromium-chromedriver
ENV CHROME_BIN="/usr/bin/chromium-browser" \
    CHROME_DRIVER="/usr/bin/chromedriver"
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]