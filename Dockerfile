# Use an official Python runtime as a parent image
FROM python:3.11.9-alpine

# Set environment variables
ENV PYTHONUNBUFFERED True

# Set workdir
WORKDIR /src

COPY . ./

RUN pip3 install --no-cache-dir -r requirements.txt

# Command to run when image started
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]
