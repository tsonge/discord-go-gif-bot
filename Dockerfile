FROM golang:1.16

WORKDIR /go/src/app

COPY . .

RUN go build sgf_to_gif.go

RUN apt-get update -y

RUN apt-get install -y python3-pip

RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]