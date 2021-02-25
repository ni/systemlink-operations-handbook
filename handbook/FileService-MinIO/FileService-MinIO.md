# MinIO as storage provider for the FileService

SystemLink FileService allows you to configure and use the Amazon S3 cloud storage instead of a file share. While NI officially addresses the Amazon S3 cloud storage, the FileService also works with MinIO, a server-side software storage stack that is compatible with Amazon S3.

To use MinIO with SystemLink, you need SystemLink version 2020 R3 or later.

To use MinIO as a storage provider, set up the MinIO server and configure the File Service to use that server.

## Running MinIO server

1. In order to run the MinIO server, download the server from the [MinIO website](https://min.io/download). From the command line, run the following command to run the server:

    ```bash
    minio server <PathToRootFolder>
    ```

2. After starting the MinIO server, connect to the endpoint that is printed out in the command line by using a web browser and create a bucket by using the `+` button in the right bottom corner. This is only required if you run the MinIO server for the first time.

    !!! note "Note"
        - It is recommended to set non-default access key and secret key. You can do that by setting the environment variables `MINIO_ACCESS_KEY` and `MINIO_SECRET_KEY`.
        - There's no bucket region necessary for using MinIO, but you have to apply a bucket region for the FileService to work. Just use `us-east-1`.
        - Any of the three endpoints in the first line of the minio server output are usable as `S3BackEndSecretKey` (for localhost given your client is on the same machine as the MinIO server).

Detailed information on how to run the server, follow instructions from the [MinIO Quickstart guide](https://docs.min.io/docs/minio-quickstart-guide.html).

## Configuring FileService

Follow the instruction from [the documentation on uploading files to S3](https://www.ni.com/documentation/de/systemlink/latest/data/uploading-files-to-amazon-s3) to configure the FileService.

Additionally to that, there are another two undocumented settings required only when using MinIO:

- `S3BackEndServiceUrl`: Set this value to ip:port of the MinIO server
- `S3ForcePathStyle`: Set this value to `True`

<!-- markdownlint-disable -->
<details>
<summary>Example Code</summary>
<!-- markdownlint-enable -->

```bash
"UseS3BackEnd" : "True”,
"S3BackEndBucketRegion" : "us-east-1",
"S3BackEndBucketName" : "<YourBucket>",
"S3BackEndAccessKeyId" : "<YourAccessKey>",
"S3BackEndSecretKey" : "<YourSecretKey>",
"S3BackEndFolderName" : "",
"S3BackEndServiceUrl" : "<YourServerIP>",
"S3ForcePathStyle" : "True"
```

</details>

Paste the example code to the JSON configuration at
`C:\ProgramData\National Instruments\Skyline\Config\FileIngestion.json`
and replace the placeholders with your actuals values.

Now, you’re ready to go. Restart the entire `NI SystemLink Service Manager`.
