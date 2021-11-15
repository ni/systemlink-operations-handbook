# Upgrading and Migrating SystemLink Server

Upgrading to a new version or migrating between SystemLink Servers is a common practice for many deployments. These processes can create risk, and the goal of this chapter is to prepare system administrators to complete this operation in the lowest risk manner possible. A constant throughout this process is to retain a fully operable SystemLink Server in cases of issues during an upgrade or migration that prevent the new instance of SystemLink Server from being used.

!!!important "Using Virtual Machines for SystemLink Deployments"
    It is recommended to run SystemLink Server, attached file stores, and databases within virtual machines. Virtual machines simplify the creation and restoration of backups. The use of other tools to facilitate the backup of bare metal machines, e.g.non-virtual machines is outside the scope of this chapter.

## Assumptions and Prerequisites

- A server running SystemLink 2021 R1 or greater

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

    - All servers, file stores, and databases running in virtualized environments

    - Removable storage volumes or device

## Preparing for Upgrade or Migration

Prior to attempting any upgrade or migration you should backup your server and any remote data stores. Failure to create backup increases the risk of unplanned downtime in the case of issues during the upgrade or migration process.

!!!note "Single Node versus Multi Node Configurations"
    **Single node** refers to the SystemLink Server configuration where the application server, file storage, and databases used by SystemLink are all installed on the same Windows server. This is the default configuration for SystemLink Server.

    **Multi node** refers to configurations where the file store or databases used by SystemLink are running on distinct hardware from the SystemLink application server. This is the recommended configuration for all production deployments.

### NI-SystemLink-Migration Command Line Utility

The workflows for upgrade and migration make use of the SystemLink command line migration tool, `nislmigrate`. Refer to the readme at the [NI-SystemLink-Migration](https://github.com/ni/NI-SystemLink-Migration) GitHub repo for details on installing and using this tool.

!!!note "Argument Flags for `nislmigrate`"
    `nislmigrate` supports capturing data from individual services as well as all installed services using the `--all` argument flag. For brevity `--all` is used most workflows in this chapter. Depending on your needs you may replace the `--all` argument flag with one or more of the individual service argument flags.

## Recommended Upgrade and Migrations Workflows for your deployment

This chapter recommends workflows for the following upgrade and migration scenarios. In all scenarios you should plan for some downtime of your SystemLink Server, but by following these recommendations you should minimize this planned downtime.

- [Single Node Upgrade](#single-node-upgrade)
- [Single Node to Multi Node Migration](#single-node-to-multi-node-migration)
    - [Single Node to Multi Node with MongoDB](#single-node-to-multi-node-with-mongodb)
    - [Single Node to Multi Node with File Storage](#single-node-to-multi-node-with-file-storage)
    - [Single Node to Multi Node with PostGreSQL](#single-node-to-multi-node-with-postgresql)
- [Upgrading Multi node configurations (MongoDB, PostGreSQL, File Share/S3)](#upgrading-multi-node-configurations-mongodb-postgresql-file-shares3)
- [Seamless cut-over](#seamless-cut-over)

!!!note "Storing Captured Data"
    For upgrades and migrations for a SystemLink Server with a small amount of data you may be able to use `nislmigrate` to backup your data to the local file system of your SystemLink Server. For SystemLink Servers with a large amount of data be aware `nislmigrate` could exhaust the local storage on the server. This can mitigated by using an attached volume. **This document assumes this will be needed and refers to this attached volume as `D:\` in each workflow.**

## Single Node Upgrade

This workflow describes steps to upgrade a single node deployment of SystemLink Server.

The SystemLink NI Package Manager Installers (NIPM) supports in-place upgrades of SystemLink Server. An in place upgrade is one where the upgrade is run directly on your current SystemLink Server. For production deployments of SystemLink Server this is not recommended. If you pursue this option it is highly recommended you backup your server prior to the upgrade. This backup is an essential fallback should an issue occur during upgrade that leaves your SystemLink Server in a bad state.

For single node upgrades, NI recommends pairing the upgrade with a migration. This mitigates risks of issues during the upgrade by ensuring your original SystemLink Server remains in an operable state.

1. Backup your SystemLink Server.

1. Attach a volume to store data captured by `nislmigrate`. This will be referenced as `D:\`.

1. Install `nislmigrate`.

1. Run the command `nislmigrate capture --all --secret <your secret> --dir D:\migration`.

    !!!note
        While `nislmigrate` runs all SystemLink services are stopped. Plan ahead for this downtime of your SystemLink server. When the capture is completed, SystemLink services will be restarted automatically.

1. Detach `D:\`.

    !!!note
        At this point in the workflow your original SystemLink Server is in an operable state. Be aware if any new data is created or ingested by SystemLink Server at this time it will not be available to your new server.

1. Provision a new Window server for SystemLink.

1. Install and configure the new version of SystemLink Server.

1. Install `nislmigrate` on your new SystemLink Server.

1. Attach the `D:\` volume used to capture data from your original SystemLink Server.

1. Run the command `nislmigrate restore --all --secret <your secret> --dir D:\migration`.

1. Verify your new SystemLink Server has all the expected migrated data.

## Single Node to Multi Node Migration

This section describes workflows used when you intend to upgrade or migrate from a single node SystemLink Server configuration to a multi node SystemLink server configuration that makes use of a dedicated servers for MongoDB, PostGreSQL, or file storage. While not required, these migration workflows include provisioning a new SystemLink Server. This is done to reduce risk and ensure your original SystemLink Server is always in an operable state.

### Single Node to Multi Node with MongoDB

This workflow describes steps to upgrade a single node deployment of SystemLink Server to a multi node deployment where the MongoDB instance used by SystemLink is hosted on a its own server or replica set.

1. Backup your SystemLink Server.

1. Attach a volume to store data captured by `nislmigrate`. This will be referenced as `D:\`.

1. Install `nislmigrate`.

1. Run the command `nislmigrate capture --all --secret <your secret> --dir D:\migration`.

1. Detach `D:\`.

    !!!note
        At this point in the workflow your original SystemLink Server is in an operable state. Be aware if any new data is created or ingested by SystemLink Server at this time it will not be available to your new server.

1. Provision a new Windows server for SystemLink.

1. Provision a new MongoDB server or replica set.

1. Install and configure the same or a newer version of SystemLink Server.

1. Configure SystemLink to use the newly created MongoDB server or replica set.

1. Install `nislmigrate` on your new SystemLink Server.

1. Attach the `D:\` volume used to capture data from your original SystemLink server.

1. Run the command `nislmigrate restore --all --secret <your secret> --dir D:\migration`.

1. Verify your new SystemLink Server has all the expected migrated data.

### Single Node to Multi Node with File Storage

This workflow describes steps to upgrade a single node deployment of SystemLink Server to a multi node deployment where the file storage instance used by SystemLink is hosted on a a dedicated NAS, SAN, or AWS S3.

1. Backup your SystemLink Server.

1. Attach a volume to store data captured by `nislmigrate`. This will be referenced as `D:\`.

1. Install `nislmigrate`.

1. Run the command `nislmigrate capture --all --secret <your secret> --dir D:\migration`.

1. Detach `D:\`.

    !!!note
        At this point in the workflow your original SystemLink Server is in an operable state. Be aware if any new data is created or ingested by SystemLink Server at this time it will not be available to your new server.

1. Provision a new file store for SystemLink.

1. Install and configure the same or a newer version of SystemLink Server.

1. Configure SystemLink to use the newly created file storage instance.

1. Install `nislmigrate` on your new SystemLink Server.

1. Attach the `D:\` volume used to capture data from your original SystemLink server.

1. Run the command `nislmigrate restore --all --secret <your secret> --change-file-store-root <new root> --dir D:\migration`.

    !!!note
        The `--change-file-store-root` argument flag is needed to update the file meta data the new root location of your file storage. This could be a new drive letter, UNC path, or S3 URL depending on your configuration. If this step is not complete you will be able to view file meta data (name, properties, etc), but you will not be able to preview or download files.

1. Verify your new SystemLink Server has all the expected migrated data.

### Single Node to Multi Node with PostGreSQL

This workflow describes steps to upgrade a single node deployment of SystemLink Server to a multi node deployment where the PostGreSQL instance used by the SystemLink Test Monitor service is hosted on a its own server or replica set.

As of SystemLink 21.5.TODO VERSION NUMBER SystemLink supports using PostGreSQL as the database backing the Test Monitor service. This configuration is optional, but provides significant performance improvements. `nislmigrate` does not yet support migrating PostGreSQL directly.

The Test Monitor Service itself performs the migration of test steps, test results, and product from MongoDB to PostGreSQL. If you intend on utilizing a single node configuration the steps for this migration are the same as described in [**Single Node Migration**](#single-node-migration). Use the following workflow if you intend on migrating or upgrading to a new server and utilize a multi node configuration where PostGreSQL is hosted on a dedicated server or replica set.

1. Backup your SystemLink Server.

1. Attach a volume to store data captured by `nislmigrate`. This will be referenced as `D:\`.

1. Install `nislmigrate`.

1. Run the command `nislmigrate capture --all --secret <your secret> --dir D:\migration`.

1. Detach `D:\`.

    !!!note
        At this point in the workflow your original SystemLink Server is in an operable state. Be aware if any new data is created or ingested by SystemLink Server at this time it will not be available to your new server.

1. Provision a new Windows server for SystemLink.

1. Provision a PostGreSQL server or replica set.

1. Install and configure the new version of SystemLink Server that supports PostGreSQL.

    !!!important
        If you are using the single node configuration for SystemLink the migration from the local instances of MongoDB to PostGreSQL begins automatically. If you are in a multi node configuration where a dedicated MongoDB server or replica set is used, you must specify the PostGreSQL instance for SystemLink to use before the MongoDB to PostGreSQL migration can occur. The next step in this workflow assumes you are in this multi node configuration.

1. Configure SystemLink to use the newly created PostGreSQL server or replica set and click **Apply**. Refer to [Connecting to a Remote PostgreSQL Database](https://www.ni.com/documentation/en/systemlink/latest/setup/remote-postgres-databse/) for this step.

1. Install `nislmigrate` on your new SystemLink Server.

1. Attach the `D:\` volume used to capture data from your original SystemLink server.

1. Run the command `nislmigrate restore --all --secret <your secret> --dir D:\migration`

    !!!note
        After this step SystemLink will migrate your test steps, results, and products from MongoDB to PostGreSQL. Depending on the size of your data set this process may take some time.

1. Verify your new SystemLink Server has all the expected migrated data.

## Upgrading Multi node configurations (MongoDB, PostGreSQL, File Share/S3)

The following workflow describes upgrading a SystemLink server that has been configured to use a dedicated MongoDB server or replica set, a dedicated PostGreSQL server or replica set, and a dedicated file store such as AWS S3.

1. Backup your SystemLink Server, MongoDB server or replica set, PostGreSQL replica set, and file store.

    !!!note
        If S3 is used as your file store the backup step is not needed since this managed internally by AWS.

1. Attach a volume to store data captured by `nislmigrate`. This will be referenced as `D:\`.

1. Install `nislmigrate`.

1. Run the command `nislmigrate capture --tags --dir D:\migration`.

    !!!note
        While most of the data is external to SystemLink, the tag current value continues to be stored on the app server. Therefore this `nislmigrate` command must be used to ensure that data is not lost during the migration.

1. Detach `D:\`.

    !!!note
        At this point in the workflow your original SystemLink Server is in an operable state. Be aware if any new data is created or ingested by the SystemLink server at this time it will not be available to your new server.

1. Provision a new Windows server for SystemLink.

1. Provision a MongoDB server or replica set from the backup previously created.

1. Provision a PostGres server or replica set from the backup previously created.

    !!!note
        The previous steps prescribes using a newly created instance of your MongoDB or PostGreSQL servers. This is because SystemLink may change the internal scheme of these databases when services start post upgrade. If you do not start with a instance from a backup you will be unable to revert the MongoDB collections and PostGreSQL tables into the schemas needed for the older version of SystemLink.

1. Install and configure the new version of SystemLink Server.

1. Configure SystemLink to use the newly created MongoDB server or replica, PostGreSQL server or replica set, and existing file store.

1. Install `nislmigrate` on your new SystemLink Server.

1. Attach the `D:\` volume used to capture data from your original SystemLink server.

1. Run the command `nislmigrate restore --tags` --dir D:\migration`.

1. Verify your new SystemLink Server has all the expected migrated data.

## Seamless Cut-over

Since managed test systems are connected SystemLink it is desirable to approach upgrades or migrations such that test systems can connect to the new instance of SystemLink without manual intervention. To accomplish this the following conditions must be met.

- Migration of systems data. This is either accomplished by using the `nislmigrate` argument flags `--all` or `--systems` or by connecting a MongoDB server or replica set that contains systems data.

- The DNS name of the original SystemLink Server and the new SystemLink Server are the same.

- If NI Web Server has been configured for HTTPS, the new SystemLink Server must use the same TSL certificate as the original SystemLink Server.