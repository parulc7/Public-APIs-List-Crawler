FROM python:3

ADD scraper.py /
COPY requirements.txt /
WORKDIR /
RUN pip3 install -r requirements.txt
CMD [ "python3", "./scraper.py" ]