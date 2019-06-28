# Command to create docker container: docker run -it --name scrapy-mogi --link mongodb:mongo -t scrapy-crawler
FROM ubuntu:19.04
 
# Update Software repository
RUN apt-get update

RUN apt install xauth -y

# RUN xauth add "tommy/unix:0  MIT-MAGIC-COOKIE-1  c75033c16d731bb153ea71545e450594"

RUN apt install firefox -y

# Install nginx, php-fpm and supervisord from ubuntu repository
RUN apt-get install -y python3 python3-pip

RUN pip3 install pymongo selenium requests timeout_decorator

