FROM python:3
ENV PYTHONUNBUFFERED 1

#　ビルド時に/codeというディレクトリ作成
RUN mkdir /portfolio3
WORKDIR /portfolio3

#　requirements.txtを/code/にコピー
COPY requirements.txt /portfolio3/
#　requirements.txtを基にパッケージリストをインストール
RUN pip install -r requirements.txt
COPY . /portfolio3/

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN pip install --no-cache-dir python-dotenv

