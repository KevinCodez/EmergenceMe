FROM alpine:latest
RUN apk update && apk add --no-cache python3 py3-pip firefox xvfb dbus
ENV GECKODRIVER_VERSION=0.36.0
RUN wget -O geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v${GECKODRIVER_VERSION}/geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz \
    && tar -xzf geckodriver.tar.gz -C /usr/local/bin/ \
    && rm geckodriver.tar.gz
ENV FIREFOX_BIN="/usr/bin/firefox"
ENV DISPLAY=:99
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"
WORKDIR /app
COPY . /app
RUN pip3 install --no-cache-dir -r requirements.txt
CMD ["python3", "-u", "main.py"]