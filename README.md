## ■ 成果物

- 都道府県データ一覧  
→ https://masakazu-hirano.notion.site/9ba3abda21bd4b3783f9ab4022a7b68c?v=65a3e9c979a64b73af794ef7855e46b2
- 市区町村データ一覧  
→ https://masakazu-hirano.notion.site/a5cfe0cd41034dfa86ccbcf8a98567b8?v=5a85097b120a4bac9a06bbcc32a7b18a

---

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
