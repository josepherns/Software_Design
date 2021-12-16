#!/bin/bash
mkdir tempdir
mkdir tempdir/templates
mkdir tempdir/static

cp School.sqlite tempdir/.
cp app.py tempdir/.
cp -r templates/* tempdir/templates/.
cp -r static/* tempdir/static/.
cp requirements.txt tempdir/.

echo "FROM python" >> tempdir/Dockerfile
echo "COPY requirements.txt /home/myapp/" >>tempdir/Dockerfile

echo "COPY  ./static /home/myapp/static/" >> tempdir/Dockerfile
echo "COPY  ./templates /home/myapp/templates/" >> tempdir/Dockerfile
echo "COPY  app.py /home/myapp/" >> tempdir/Dockerfile
echo "RUN pip install -r /home/myapp/requirements.txt" >> tempdir/Dockerfile

echo "EXPOSE 8080" >> tempdir/Dockerfile
echo "CMD python3 /home/myapp/app.py" >> tempdir/Dockerfile

cd tempdir
docker build -t midtermproject .
docker run -t -d -p 8080:8080 --name midterm midtermproject
docker ps -a
