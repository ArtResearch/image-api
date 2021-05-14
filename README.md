# image-thumbnail-api
API to retrieve images from the platform and materialize thumbnails to AWS S3

Requirements:

- SPARQL construct statement that pulls in list of image thumnails in two sizes:
200px (for the results page when performing searches
500px (for the Photo/Artwork templates for visualization)
- uploads the images to an AWS S3 bucket
- materializes the image thumbnail data to the graph for visualization
