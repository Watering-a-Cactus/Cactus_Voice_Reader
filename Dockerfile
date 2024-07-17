# 베이스 이미지 설정
FROM rasa/rasa:latest-full

# 작업 디렉토리 설정
WORKDIR /app

# 루트 사용자로 필요한 시스템 종속성 설치
USER root

RUN apt-get update && \
    apt-get install -y default-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 환경 변수 설정
ENV JAVA_HOME /usr/lib/jvm/default-java
ENV PATH $JAVA_HOME/bin:$PATH

# Rasa 프로젝트 파일 복사
COPY ./rasa /app

# requirements.txt 파일 복사
COPY ./requirements.txt /app/requirements.txt

# 루트 사용자로 pip 종속성 설치
RUN pip install --no-cache-dir -r /app/requirements.txt

# 작업 디렉토리의 권한을 변경하여 non-root 사용자로 실행할 수 있도록 설정
RUN chown -R 1000:1000 /app

# Rasa 텔레메트리 비활성화
RUN rasa telemetry disable

# Rasa 서버 실행
CMD [ "run", "--enable-api", "--cors", "*"]

# non-root 사용자로 전환
USER 1000
