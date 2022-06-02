FROM python:3.9.11-alpine3.14

# set a directory for the app
WORKDIR /home/microblog

# copy requirement files
COPY requirements.txt /home/microblog/requirements.txt

# copy all the files to the container
COPY . .

# install dependencies
RUN pip install -r requirements.txt

# tell the port number the container should expose
EXPOSE 8000

# run the command
CMD ["python3", "microblog.py" ]