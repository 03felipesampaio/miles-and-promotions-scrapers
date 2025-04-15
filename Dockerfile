FROM python:3.13-alpine

# Set the working directory
WORKDIR /app
# Copy the requirements file into the container
COPY requirements.txt .
# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copy the rest of the application code into the container
COPY ./scripts .

ENTRYPOINT [ "python3" ]
CMD [ "crawlers/crawler_livelo_partners.py" ]