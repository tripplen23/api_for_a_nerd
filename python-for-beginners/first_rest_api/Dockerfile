# start by pulling the python image
FROM python:3.8-alpine
EXPOSE 5000
WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]

# To build: docker build -t flask-smorest-api .
# ||
# To build: docker build -t rest-apis-flask-python .
# To run: docker run -dp 5005:5000 flask-smorest-api
# ||
# To run: docker run -dp 5005:5000 rest-apis-flask-python

# The problem with that is, every time that we update the code,
    # we have to rebuild and rerun -> 
    # Solution: volume (for only local development, not for deployment)
# docker run -dp 5005:5000 -w /app -v "$(pwd):/app" flask-smorest-api
# docker run -dp 5005:5000 -w /app -v "$(pwd):/app" rest-apis-flask-python