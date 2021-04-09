# Leverage Cloud File Storage with MinIO

SystemLink File Service allows you to configure and use the Amazon S3 cloud storage instead of a file share. While NI officially addresses the Amazon S3 cloud storage, the File Service also works with MinIO, a server-side software storage stack that is compatible with Amazon S3.

To use MinIO with SystemLink, you need SystemLink version 2020 R3 or later.

To use MinIO as a storage provider, set up the MinIO server on a system that you would like to upload files to. This can be the same machine as the SystemLink server or your own dedicated server. Then, configure the File Service to use that server.

## Running MinIO server

1. Download the server application from the [MinIO website](https://min.io/download).

2. From the command line, run the following command to run the server:

    ```bash
    minio server <PathToRootFolder>
    ```

    <figure>
    <img src="../../img/minio-server.png" width="500" />
    <figcaption>Running a minio server.</figcaption>
    </figure>

3. When starting the MinIO server for the first time, use a web browser and navigate to the URL that the command line prints out. Create a bucket by clicking the `+` button in the right bottom corner.

    !!! note "Note"
        - It is recommended to set non-default access key and secret key. You can do that by setting the environment variables `MINIO_ACCESS_KEY` and `MINIO_SECRET_KEY`. Run the following commands from the command line to start a server pointing at C:\minio with your individual access and secret keys:
        ```
        set MINIO_ACCESS_KEY=YourAccessKey
        set MINIO_SECRET_KEY=YourSecretKey
        minio server C:\minio
        ```
        - There's no bucket region necessary for using MinIO since it is not hosted on an actual AWS S3 storage. You still have to apply a valid bucket region for the File Service to work. You can use any valid Amazon S3 region, like `us-east-1` or `eu-central-1`.
        - Any of the three endpoints in the first line of the minio server output are usable as `S3BackEndSecretKey` (for localhost given your client is on the same machine as the MinIO server).

For detailed information on how to run the server, follow the instructions from the [MinIO Quickstart guide](https://docs.min.io/docs/minio-quickstart-guide.html).

## Configuring File Service

1. Follow the instructions from [the documentation on uploading files to S3](https://www.ni.com/documentation/de/systemlink/latest/data/uploading-files-to-amazon-s3) to configure the File Service.

2. In addition to that, there are two additional settings required only when using MinIO. Add these settings to the JSON configuration file at `C:\ProgramData\National Instruments\Skyline\Config\FileIngestion.json`:

    - `S3BackEndServiceUrl`: Set this value to ip:port of your MinIO server
    - `S3ForcePathStyle`: Set this value to `True`

    You can paste the example code below to the config file and replace the placeholders with your actuals values.

    ```bash
    "UseS3BackEnd" : "True",
    "S3BackEndBucketRegion" : "us-east-1",
    "S3BackEndBucketName" : "<YourBucket>",
    "S3BackEndAccessKeyId" : "<YourAccessKey>",
    "S3BackEndSecretKey" : "<YourSecretKey>",
    "S3BackEndFolderName" : "",
    "S3BackEndServiceUrl" : "<YourServerIP>",
    "S3ForcePathStyle" : "True"
    ```

3. In the `NI SystemLink server configuration` dialog, go to the `NI SystemLink Service Manager` tab and click `Restart` to apply the settings you made in the JSON file.
