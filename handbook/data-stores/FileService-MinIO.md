# Leverage File Service S3 for on-premises storage

SystemLink File Service allows you to configure and use the Amazon S3 cloud storage instead of a file share. The File Service will also work with MinIO, a server-side software storage stack that is compatible with Amazon S3.

You can configure and use an on-premises MinIO server. Due to limitations, however, connecting to GCS or Azure using the MinIO gateway is unsupported.

To use MinIO with SystemLink, you need SystemLink version 2020 R3 or later.

To use MinIO as a storage provider, set up the MinIO server on a system that you would like to upload files to. This can be the same machine as the SystemLink server or your own dedicated server. Then, configure the File Service to use that server.

## Running MinIO server

1. Download the server application from the [MinIO website](https://min.io/download).

2. Since [MinIO discourages use of the default credentials](https://docs.min.io/minio/baremetal/security/IAM/iam-users.html#:~:text=If%20these%20variables%20are%20unset,credentials%20regardless%20of%20deployment%20environment.), you should change the access key and secret key. To do this, define the environment variables `MINIO_ACCESS_KEY` and `MINIO_SECRET_KEY`.

3. Run the following command to start the server with individual access and secret keys:

    ```powershell
    set MINIO_ACCESS_KEY=YourAccessKey
    set MINIO_SECRET_KEY=YourSecretKey
    minio server C:\minio
    ```

    <figure>
    <img src="../../img/minio-server.png" width="500" />
    <figcaption>Running a minio server.</figcaption>
    </figure>

4. When starting the MinIO server for the first time, use a web browser and navigate to the URL that the command line prints out. Create a bucket by clicking the `+` button in the right bottom corner.

5. Keep the command line open to keep the MinIO server running.

For detailed information on how to run the server, follow the instructions from the [MinIO Quickstart guide](https://docs.min.io/docs/minio-quickstart-guide.html).

## Configuring File Service

1. Follow the instructions from [the documentation on uploading files to S3](https://www.ni.com/documentation/de/systemlink/latest/data/uploading-files-to-amazon-s3) to configure the File Service.

    a) Set the access key and secret key you chose when starting the MinIO server.

    b) Apply a valid bucket region. You can use any valid Amazon S3 region, like `us-east-1` or `eu-central-1`.

    c) Set the bucket name you created.

2. Add two additional settings to the JSON configuration file at `C:\ProgramData\National Instruments\Skyline\Config\FileIngestion.json`:

    - `S3BackEndServiceUrl`: Set this value to ip:port of your MinIO server. You can obtain that from the MinIO output in your command line.
    - `S3ForcePathStyle`: Set this value to `True`

    You can paste the example code below to the config file and replace the placeholders with your actual values.

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

3. In the `NI SystemLink Server Configuration` dialog, go to the `NI SystemLink Service Manager` tab and click `Restart` to apply the settings you made in the JSON file.
