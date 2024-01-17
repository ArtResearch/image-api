## Endpoints

- `/reverse-hash-image-URL`: This endpoint () takes the hash of an image URL (optionally with a `.jpg` suffix) and returns the original URL of the image in JSON format.
- `/process-image`: The  endpoint accepts an image URL (considering potential escape characters) and performs several operations:

1. **Image Downloading**:
   - Downloads the image (supports JPG, TIFF, or PNG) using the provided URL.
   - Validates the image and ensures the link is operational, handling different HTTP status codes appropriately.
   - Saves the image in a directory named "originals".
   - If the image cannot be downloaded (non-200 HTTP responses), certain RDF data parts are not materialized.
2. **Image name Hashing**:
   It hashes the url of the image to generate a name, based on this hash. This is to ensure that there are no clashes with filenames when we have a directory of millions of images.

3. **Thumbnail Generation**:
   - Creates a 200px wide JPG thumbnail for web delivery, saved in a directory named "200px".
   - Generates a 1000px wide JPG derivative, stored in a directory named "1000px".

4. **RDF Data File Generation**:
   - Produces a Turtle (TTL) formatted RDF file, named using a hash of the image URL (e.g., `abcd1234.ttl`).
   - The RDF file contains metadata about when the image was downloaded and any HTTP status codes. It is saved in a directory called "image-RDF-data".

## RDF Data Model

Utilizes a static file `image-data-model.ttl` to determine the output data model.



```
@prefix image-api: <https://artresearch.net/image-api/>.

<ImageURL> image-api:identifier "hashedImageIdentifier" ;
    image-api:thumbnail <path_to_image/hashedImageURL.jpg> ;
    image-api:date-processed "YYYY-MM-DDTHH:MM:SSZ"^^xsd:dateTime ;
    image-api:status-code <http://www.w3.org/2011/http-statusCodes#200> ;
    image-api:error-description "error description" ;
```

## Directory Structure

- `originals`, `200px`, `1000px`, `image-RDF-data`: Directories within `/image-data` for storing processed images and data.
- `image-data-model.ttl`: Located in the `/data` directory.
