# Convert2EPUB

This repository contains the implementation of an API to convert [Calibre](https://calibre-ebook.com/) files to EPUB. The followin image describes the Request and Response accepted and returned respectively from the API:

![API](img/Diagram.svg)


# 1. How to deploy the API in Google Cloud
This section explains the requirements and implementations necessary to host and deploy the containerized API localized in `root`.

### 1. Authenticate

The first step is to authenticate via `gcloud` as shown below:

```bash
gcloud init
gcloud auth application-default login
```

When entering the above commands, the respective credentials will be required for authentication.

### 2. Initialize global variables

Next, we will need to export environment variables which refer to the `PROJECT_ID` and `REGION` of the project:

```bash
export PROJECT_ID=$(gcloud config get-value project)
export REGION=us-central1
```

### 3. Create Artifact Registry to store Docker images

Next, we will create a repository for Docker images in [Artifact Registry](https://cloud.google.com/artifact-registry):

```bash
gcloud artifacts repositories create cloudrun-images \
--repository-format=docker \
--location=$REGION \
--description="images for cloud run deploy" \
--async
```

### 4. Configure local permissions

In order to connect from our premises to Artifact Registry, we need to assign the respective permissions:

```bash
gcloud auth configure-docker $REGION-docker.pkg.dev
```

This will allow us to push docker images from our local machine.
### 5. Clone the repository

```bash
git clone https://github.com/Anonymate054/CalibreConverter.git
cd CalibreConverter
```
### 6. Build the Docker image using Cloud Build

To build the image from the Dockerfile, we will use Cloud Build as shown below:

```bash
gcloud builds submit . --tag $REGION-docker.pkg.dev/$PROJECT_ID/cloudrun-images/convert2epub:latest
```

### 7. Deploy Cloud Run API

Once the image is built, we will deploy it to Cloud Run with the following command:

```bash
gcloud run deploy convert2epub \
--image $REGION-docker.pkg.dev/$PROJECT_ID/cloudrun-images/convert2epub \
--platform managed \
--region $REGION \
--port 8080 \
--allow-unauthenticated 
```

### 8. Test API

Get the URL from the deployed API similar to:  `https://convert2epub-url/convert2epub` and replace it in the URL below:

```bash

export SERVICE_URL=$(gcloud run services describe convert2epub --format='value(status.url)' --region=$REGION)

curl -X POST \
-H "Content-Type: application/json" \
-d '{
    "bucket": "my-bucket",
    "input_file_name": "file.docx",
    "output_file_name": "file.epub" 
}' $SERVICE_URL/convert2epub
```

### 9. Example

This example demonstrates how to use the deployed API. It walks through creating a new bucket in Cloud Storage, uploading a sample .docx file, using the API to convert it to EPUB, and finally downloading the converted file.

Make sure you are located in the `convert2epub/` directory for this example.

```bash
export BUCKET_NAME="$PROJECT_ID-convert2epub"
gsutil mb -p $PROJECT_ID gs://$BUCKET_NAME

gsutil cp hustle_flyer.docx gs://$BUCKET_NAME/

export SERVICE_URL=$(gcloud run services describe convert2epub --format='value(status.url)' --region=$REGION)

curl -X POST \
-H "Content-Type: application/json" \
-d '{
    "bucket": "'"$BUCKET_NAME"'",
    "input_file_name": "hustle_flyer.docx",
    "output_file_name": "hustle_flyer.epub" 
}' $SERVICE_URL/convert2epub


gsutil cp gs://$BUCKET_NAME/hustle_flyer.epub .
```

# References
- https://cloud.google.com/run/docs/building/containers
- https://cloud.google.com/artifact-registry/docs/docker/troubleshoot
- https://cloud.google.com/run/docs/deploying#gcloud
- https://github.com/sekR4/FastAPI-on-Google-Cloud-Run
- https://medium.com/@saverio3107/deploy-fastapi-with-docker-cloud-run-a-step-by-step-guide-a01c42df0fee
- https://github.com/ulises-jimenez07/convert2pdf


## Contributions

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
