# Upgrading and Migrating SystemLink Server

This chapter covers how to maintain a fully operable SystemLink Server while upgrading to a new version of SystemLink or migrating between SystemLink servers.

To simplify creating and restoring backups, NI recommends running SystemLink Server, attached file stores, and databases within virtual machines. Backing up physical machines is outside the scope of this chapter.

## Assumptions and Prerequisites

- A server running SystemLink 2021 R1 or greater. Migrating from older versions of SystemLink is not supported at this time.

- Familiarity with installing and setting up a SystemLink Server

    - [Setting up a SystemLink Server](https://www.ni.com/documentation/en/systemlink/latest/setup/)

    - [Configuring NI Web Server](https://www.ni.com/documentation/en/ni-web-server/latest/manual/configuring-ni-web-server/)

        - [Sign on with LDAP](/ldap/ldap)

        - [Single Sign-on with OpenID Connect](/openid-connect/openid-connect/)

    - Data Store Configuration

        - [MongoDB](/data-stores/mongodb/)

        - [Connecting to a Remote Mongo Database](https://www.ni.com/documentation/en/systemlink/latest/setup/remote-mongo-database/)

        - [Connecting to a Remote File Share](https://www.ni.com/documentation/en/systemlink/latest/setup/remote-file-share/)

        - [Uploading Files to Amazon Simple Storage Service (S3)](https://www.ni.com/documentation/en/systemlink/latest/data/uploading-files-to-amazon-s3/)

        - [Connecting to a Remote PostgreSQL Database](https://www.ni.com/documentation/en/systemlink/latest/setup/remote-postgres-databse/)

- Recommended

    - Virtual machines to run all servers, file stores, a databases

    - Removable storage volume or device

## Preparing for Upgrade or Migration

Before you begin, backup your server and any remote data to avoid unplanned downtime if issues occur during the upgrade or migration process.

!!!note "Single Node versus Multi Node Configurations"
    **Single node** refers to the SystemLink Server configuration where the application server, file storage, and databases used by SystemLink are all installed on the same Windows server. This is the default configuration for SystemLink Server.

    **Multi node** refers to configurations where one or more file stores or databases used by SystemLink are running on hardware distinct from the SystemLink application server. This is the recommended configuration for all production deployments.

### NI-SystemLink-Migration Command Line Utility

The workflows for upgrades and migrations makes use of the SystemLink command line migration tool, `nislmigrate`. Refer to the [NI-SystemLink-Migration](https://pypi.org/project/nislmigrate/) documentation in PyPi for details on installing and using this tool.

!!!important "Limitations of `nislmigrate`"
    The NI-SystemLin-Migration tool does not yet support migrating all data in SystemLink. [Refer to the **Supported Services** table on PyPi](https://pypi.org/project/nislmigrate/) for details.

!!!note "Argument Flags for `nislmigrate`"
    `nislmigrate` supports capturing data from individual services or can capture data from all installed services using the `--all` argument flag. For brevity `--all` is used most workflows in this chapter. Depending on your needs you may replace the `--all` argument flag with one or more of the individual service argument flags.

### Upgrading from SystemLink 21.3 or earlier to SystemLink 21.5 or later

After upgrading from SystemLink 21.3 or earlier to SystemLink 21.5 or later, SystemLink will migrate your test steps, results, and products from MongoDB to PostgreSQL. Depending on the size of your data set this process may take some time. For reference, a typical server takes less than one hour to migrate 5 million steps. To check the step count on your server, you can use the Mongo shell or a client such as Robo 3T. The credentials required for connecting to the database can be found in `C:\ProgramData\National Instruments\Skyline\Config\TestMonitor.json`. Use the step count to roughly estimate the expected migration time. Note that system resources and network connectivity will impact the migration time.

The TestMonitor service will display a status of **Migrating** during this process. You can view detailed status of this process with `C:\ProgramData\National Instruments\Skyline\Logs\log.txt`.

If you see an error, double check your connection string and restart SystemLink Service Manager.

## Recommended Upgrade and Migration Workflows for your deployment

While you should plan for some downtime of your SystemLink Server, you can minimize that downtime by following these recommendations.

- [Single Node Upgrade](#single-node-upgrade)
- [Single Node to Multi Node Migration](#single-node-to-multi-node-migration)
    - [Single Node to Multi Node with MongoDB](#single-node-to-multi-node-with-mongodb)
    - [Single Node to Multi Node with File Storage](#single-node-to-multi-node-with-file-storage)
    - [Single Node to Multi Node with PostgreSQL](#single-node-to-multi-node-with-postgresql)
- [Upgrading Multi node configurations (MongoDB, PostgreSQL, File Share/S3)](#upgrading-multi-node-configurations)
- [Seamless cut-over](#seamless-cut-over)

If you have a SystemLink Server with a small amount of data, you can use `nislmigrate` to backup your data to the local file system of your SystemLink Server. For SystemLink Servers with a large amount of data, you may need to use an attached volume since the backup created by `nislmigrate` may exhaust the local storage. This document assumes that you are using an attached volume and refers to the volume as `D:\` in each workflow.

!!!important "Storing Sensitive Data"
    The migration of systems data (`--all` or `--systems`) will migrate the private key used decrypt communication between your SystemLink server and test systems. In this case, `nislmigrate` requires the use of the `--secret` argument to encrypt this key. While this provides some assurances of the security of this private key, it is the users responsibility to ensure this private key and sensitive production data are properly handled during migration and after the process is complete.

### Single Node Upgrade

Complete the following steps to upgrade a single node deployment of SystemLink Server.

Though the NI Package Manager (NIPM) installer for SystemLink supports in-place upgrades where the upgrade runs directly on your current SystemLink Server, NI does not recommend this option. If you choose this option, ensure that you backup your server before beginning the upgrade.

For single node upgrades, NI recommends upgrading and migrating at the same time to mitigate issues during the upgrade by ensuring your original SystemLink Server remains operable.

If migrating from SystemLink 21.3 or earlier to SystemLink 21.5 or later, your Test Monitor data must be migrated from MongoDB to PostgreSQL before the service can start. If Test Monitor is using the local instance of MongoDB stored in the default location, the migration will occur automatically. If not, the migration must be approved on the TestMonitor tab in the **NI SystemLink Server Configuration** application.

1. Backup your SystemLink Server.

1. Attach a volume to store data captured by `nislmigrate`. This will be referenced as `D:\`.

1. Install `nislmigrate`.

1. Run the command `nislmigrate capture --all --secret <your secret> --dir D:\migration`.

    !!!note
        While `nislmigrate` runs all SystemLink services are stopped. Plan ahead for this downtime of your SystemLink server. When the capture is completed, SystemLink services will be restarted automatically.

1. Detach `D:\`.

    !!!note
        After this step, your original SystemLink Server is still operable, but any new data created or consumed by SystemLink Server at this time will not be available to your new server.

1. Provision a new Windows server for SystemLink.

1. Install and configure the new version of SystemLink Server.

1. Install `nislmigrate` on your new SystemLink Server.

1. Attach the `D:\` volume used to capture data from your original SystemLink Server.

1. Run the command `nislmigrate restore --all --secret <your secret> --dir D:\migration`.

1. Verify your new SystemLink Server has all the expected migrated data.

### Single Node to Multi Node Migration

This section describes workflows to prepare to upgrade or migrate from a single node SystemLink Server configuration to a multi node SystemLink Server configuration that makes use of dedicated servers for MongoDB, PostgreSQL, or file storage.

#### Single Node to Multi Node with MongoDB

Complete the following steps to upgrade a single node deployment of SystemLink Server to a multi node deployment where the MongoDB instance used by SystemLink is hosted on its own server or replica set.

1. Backup your SystemLink Server.

1. Attach a volume to store data captured by `nislmigrate`. This will be referenced as `D:\`.

1. Install `nislmigrate`.

1. Run the command `nislmigrate capture --all --secret <your secret> --dir D:\migration`.

1. Detach `D:\`.

    !!!note
        After this step, your original SystemLink Server is still operable, but any new data created or consumed by SystemLink Server at this time will not be available to your new server.

1. Provision a new Windows server for SystemLink.

    !!!note
        While not required, provisioning a new SystemLink Server ensures your original SystemLink Server is always in an operable state.

1. [Provision a new MongoDB server or replica set](/data-stores/mongodb/#multi-node-deployments).

1. Install and configure the same or a newer version of SystemLink Server.

1. Configure SystemLink to use the newly created MongoDB server or replica set.

1. Install `nislmigrate` on your new SystemLink Server.

1. Attach the `D:\` volume used to capture data from your original SystemLink server.

1. Run the command `nislmigrate restore --all --secret <your secret> --dir D:\migration`.

1. Verify your new SystemLink Server has all the expected migrated data.

#### Single Node to Multi Node with File Storage

Complete the following steps to upgrade a single node deployment of SystemLink Server to a multi node deployment where the file storage instance used by SystemLink is hosted on sa dedicated NAS, SAN, or AWS S3.

1. Backup your SystemLink Server.

1. Attach a volume to store data captured by `nislmigrate`. This will be referenced as `D:\`.

1. Install `nislmigrate`.

1. Run the command `nislmigrate capture --all --secret <your secret> --dir D:\migration`.

1. Copy the files from the original file storage location to the new file store using one of the following options.

    | Destination | Recommended Tool |
    | ----------- | ---------------- |
    | NAS | File Explorer or PowerShell |
    | SAN | File Explorer or PowerShell |
    | AWS S3 | [AWS CLI](https://aws.amazon.com/cli/) |

1. Detach `D:\`.

    !!!note
        After this step, your original SystemLink Server is still operable, but any new data created or consumed by SystemLink Server at this time will not be available to your new server.

1. Provision a new file store for SystemLink.

1. Install and configure the same or a newer version of SystemLink Server.

1. Configure SystemLink to use the newly created file storage location.

1. Install `nislmigrate` on your new SystemLink Server.

1. Attach the `D:\` volume used to capture data from your original SystemLink server.

1. Run the command `nislmigrate restore --all --secret <your secret> --change-file-store-root <new root> --dir D:\migration`.

    !!!note
        You must use the `--change-file-store-root argument` flag to update the file meta data the new root location of your file storage. Otherwise, you will not be able to preview or download files. Depending on your configuration, this could be a new drive letter, UNC path, or S3 URL.

        | Migration Destination | Example `nislmigrate` Command |
        | --------------------- | ------------------- |
        | New drive and directory | `nislmigrate restore --all --secret <your secret> --change-file-store-root X:\systemlink\data --dir D:\migration` |
        | UNC path | `nislmigrate restore --all --secret <your secret> --change-file-store-root \\FileShare\systemlink\data --dir D:\migration` |
        | AWS S3 | `nislmigrate restore --all --secret <your secret> --change-file-store-root s3://yours3bucket/systemlink/data/ --dir D:\migration` |

1. Verify your new SystemLink Server has all the expected migrated data.

#### Single Node to Multi Node with PostgreSQL

Complete the following steps to upgrade a single node deployment of SystemLink Server to a multi node deployment where the PostgreSQL instance used by the SystemLink Test Monitor service is hosted on a its own server or replica set. The Test Monitor Service performs the migration of test steps, test results, and product from MongoDB to PostgreSQL.

As of SystemLink 21.5, SystemLink supports using a local or external PostgreSQL database for the Test Monitor service. `nislmigrate` does not yet support migrating between PostgreSQL servers or replica sets.

1. If Test Monitor is using MongoDB in its default location (`C:\ProgramData\National Instruments\Skyline\NoSqlDatabase`), use the **NI SystemLink Server Configuration** to manually specify the database location as the default. This will prevent the Test Monitor service from automatically migrating the MongoDB data to the local PostgreSQL after upgrading.

1. Backup your SystemLink Server.

1. Attach a volume to store data captured by `nislmigrate`. This will be referenced as `D:\`.

1. Install `nislmigrate`.

1. Run the command `nislmigrate capture --all --secret <your secret> --dir D:\migration`.

1. Detach `D:\`.

    !!!note
        After this step, your original SystemLink Server is still operable, but any new data created or consumed by SystemLink Server at this time will not be available to your new server.

1. Provision a new Windows server for SystemLink.

1. Provision a PostgreSQL server or replica set.

1. Install and configure SystemLink 21.5 or later.

1. Install `nislmigrate` on your new SystemLink Server.

1. Attach the `D:\` volume used to capture data from your original SystemLink server.

1. Run the command `nislmigrate restore --all --secret <your secret> --dir D:\migration`.

1. Open the **NI SystemLink Server Configuration** application.

1. Navigate to PostgreSQLDatabase and connect to your external PostgreSQL database. See the [SystemLink manual](https://www.ni.com/documentation/en/systemlink/latest/setup/remote-postgres-databse/) for more details.

1. Navigate to TestMonitor, approve the migration, and click **Apply** to begin the migration.

1. Verify your new SystemLink Server has all the expected migrated data.

### Upgrading Multi Node Configurations

Complete the following steps to upgrade a SystemLink Server instance that has been configured to use a dedicated MongoDB server or replica set, a dedicated PostgreSQL server or replica set, and a dedicated file store such as AWS S3.

!!!note
    NI recommends using dedicated external data stores for all production deployments. The following workflow assumes you are in this configuration when upgrading SystemLink Server. Refer to the other workflows in this document to migrate your data into this configuration.

1. Backup your SystemLink Server, MongoDB server or replica set, PostgreSQL server or replica set, and file store.

    !!!note
        If S3 is used as your file store the backup step is not needed since this managed internally by AWS.

1. Attach a volume to store data captured by `nislmigrate`. This will be referenced as `D:\`.

1. Install `nislmigrate`.

1. Run the command `nislmigrate capture --tags --dir D:\migration`.

    !!!note
        While most of the data is external to SystemLink, tag current values are stored on the app server. Therefore this `nislmigrate` argument flag must be used to ensure that data is not lost during the migration. Be aware this operation will also replace tag history data stored in MongoDB.

1. Detach `D:\`.

    !!!note
        After this step your original SystemLink Server is in an operable state. Be aware if any new data is created or ingested by the SystemLink server at this time it will not be available to your new server.

1. Provision a new Windows server for SystemLink.

1. Provision a MongoDB server or replica set from the backup previously created.

1. Provision a PostgreSQL server or replica set from the backup previously created.

    !!!note
        The previous steps prescribe using a newly created instance of your MongoDB or PostgreSQL servers. This is because SystemLink may change the internal schema of these databases when services start post upgrade. If you do not start with an instance from a backup you will be unable to revert the MongoDB collections and PostgreSQL tables into the schemas needed for the older version of SystemLink.

1. Install and configure the new version of SystemLink Server.

1. Configure SystemLink to use the newly created MongoDB server or replica set, PostgreSQL server or replica set, and existing file store.

1. Install `nislmigrate` on your new SystemLink Server.

1. Attach the `D:\` volume used to capture data from your original SystemLink server.

1. Run the command `nislmigrate restore --tags --dir D:\migration`.

1. Verify your new SystemLink Server has all the expected migrated data.

## Seamless Cut-over

Since managed test systems are connected SystemLink test systems can connect to the new instance of SystemLink without manual intervention. To accomplish this the following conditions must be met:

- Migration of systems data.

    - This is either accomplished by using the `nislmigrate` argument flags `--all` or `--systems`. These migration arguments must be used even in cases where an external MongoDB server or replica set is used. Otherwise the systems management private key is not retained and test systems will need to be approved again to connect to your SystemLink server.

- The DNS name of the original SystemLink Server and the new SystemLink Server are the same.

- If NI Web Server has been configured for HTTPS, the new SystemLink Server must use the same TLs certificate as the original SystemLink Server.
