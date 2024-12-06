FROM python:3.9-slim

#sets the working directory in the container
WORKDIR /app

#copies requirements file into the container
COPY requirements.txt /app/

# installs dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copies source code into the container
COPY . /app/

# sets environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development  # You can change this to "production" in production environments

# exposes port that flask will run on (default is 5000)
EXPOSE 5000

# command to run your Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
