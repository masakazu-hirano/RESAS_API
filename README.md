## ■ 技術仕様

- Python Version: 3.11.3
- pip Version: 23.1.2

  - ライブラリ一覧
    - python-dotenv  
    → https://pypi.org/project/python-dotenv
    - requests  
    → https://pypi.org/project/requests

- Notion API  
→ https://developers.notion.com

## ■ 開発環境

- Docker Version: 23.0.5
  ```Dockerfile
  FROM python:3.11.3

  COPY . /usr/local/src
  WORKDIR /usr/local/src

  RUN apt-get update \
      && apt-get install -y systemctl cron vim git \
      && systemctl start cron

  RUN git config --global user.name 'GitHub ユーザー名' \
      && git config --global user.email @users.noreply.github.com

  RUN pip install --upgrade pip \
      && pip install -r requirements.txt
  ```

- Docker Compose Version: 2.17.3
  ```compose.yaml
  version: '3.8'

  services:
    'Docker サービス名':
      container_name: 'Docker コンテナ名'
      image: 'Docker イメージ名':latest
      build:
        context: .
      volumes:
        - .:/usr/local/src:delegated
      tty: true
  ```
