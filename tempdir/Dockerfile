FROM python
RUN pip install flask
COPY  ./static /home/myapp/static/
COPY  ./templates /home/myapp/templates/
COPY app.py  /home/myapp/
EXPOSE 1010
CMD python3 /home/myapp/app.py
