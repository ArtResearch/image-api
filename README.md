# Image-api

This repository contains a dockerized application to download images from IIIF servers, generate thumbnails for delivery on the web, and produce RDF files for loading up into the graph database for each image. Each RDF file contains info about the availability of the image from the IIIF server at the time that it was processed.

There are two containers:
- Image Processing API
- Image Queue Processor
  

# Image Processing API

This application is a FastAPI-based service for processing images. It downloads images from given URLs, generates thumbnails and other derivatives, and produces RDF data files with details about the images and their processing.

## Features

- **Image Downloading**: Downloads images from provided URLs.
- **Thumbnail Generation**: Creates thumbnails and other size variants of the images.
- **RDF Data Generation**: Produces RDF files with metadata about the images.
- **Dockerized**: The application is containerized with Docker for easy deployment.
- **Logging**: Detailed logging of the image processing steps.

## Directory Structure

```
/image-api/
│
├── image-processing-api/  # FastAPI application
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py        # Main application file
│   │   ├── routes/        # API route definitions
│   │   ├── models.py      # Pydantic models
│   │   └── utils/         # Utility functions
│   ├── Dockerfile         # Dockerfile for building the image
│   ├── requirements.txt   # Python dependencies
│   └── tests/             # Test scripts
│
├── data/                  # Data directory for RDF models
├── image-data/            # Directory for storing processed images
└── docker-compose.yml     # Docker Compose configuration
```

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Running the Application

1. **Clone the Repository**

   Clone this repository to your local machine or download the source code.

2. **Navigate to the Project Directory**

   Change into the `image-api` directory:

   ```bash
   cd image-api
   ```

3. **Environment Variables**

   Set the required environment variables. Create a `.env` file in the `image-api` directory with the following content:

   ```
   THUMBNAIL_BASE_URL=<your-thumbnail-base-url>
   ```

   Replace `<your-thumbnail-base-url>` with the actual base URL for thumbnails.

4. **Build and Run with Docker Compose**

   From the `image-api` directory, run:

   ```bash
   docker-compose up --build
   ```

   This command builds the Docker image and starts the container.

5. **Accessing the API**

   The API will be available at `http://localhost:8005`. You can make requests to the API endpoints as defined in the application.

6. **Viewing Logs**

   To view the logs, use:

   ```bash
   docker-compose logs -f
   ```

### API Endpoints

- `/process-image`: Accepts an image URL, downloads the image, generates thumbnails, and produces an RDF file.
- `/reverse-hash-image-URL/{hash}`: Given a hash, retrieves the original image URL.

### Making Changes

To make changes to the application:

1. Edit the files in the `image-processing-api` directory.
2. Rebuild the Docker container with `docker-compose up --build`.



# Image Queue Processor

(coming soon)

The aim of the image queue processor is to execute a SPARQL query to a specified SPARQL endpoint (taken from the sparql-endpoint.config file), save the response to a CSV file and then process those image URL's through the Image API endpoint. The Image processor will either retrieve images that have not yet been processed using the model "retrieve-unprocessed-images.ttl" or it will attempt to reprocess images that have returned an HTTP response that is not 200/3XX with the model "reprocess-invalid-images.ttl"
