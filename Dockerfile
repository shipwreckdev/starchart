FROM python:3.7-slim-stretch

# Install nmap.
RUN apt-get update -y && \
    apt-get install nmap -y && \
    apt-get clean

# Copy only the relevant Python files into the container.
COPY ./lib /sc/lib
COPY requirements.txt /sc
COPY main.py /sc

# Set the work directory to the app folder.
WORKDIR /sc

# Install Python dependencies.
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]
