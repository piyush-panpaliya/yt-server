FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    wget \
    xz-utils \
    unzip \
    nscd \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz 

RUN tar xvf ffmpeg-release-amd64-static.tar.xz && \
    cd ffmpeg-*-static && \
    ln -s "${PWD}/ffmpeg" /usr/local/bin/ && \
    ln -s "${PWD}/ffprobe" /usr/local/bin/

RUN rm -rf ffmpeg-release-amd64-static.tar.xz
 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x /app/start.sh

EXPOSE 5000

CMD ["/app/start.sh"]
