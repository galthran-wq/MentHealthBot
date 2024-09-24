FROM python:buster
RUN mkdir -p /usr/app
WORKDIR /usr/app
COPY . /usr/app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["./src/main.py"]
