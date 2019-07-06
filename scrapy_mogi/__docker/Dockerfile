# Command to create docker container: docker run -it --name scrapy-mogi --link mongodb:mongo -t scrapy-crawler
FROM ubuntu:19.04
 
# Update Software repository
RUN apt-get update
 
# Install nginx, php-fpm and supervisord from ubuntu repository
RUN apt-get install -y python3 python3-pip

RUN pip3 install scrapy pymongo timeout_decorator requests

