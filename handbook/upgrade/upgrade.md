# Upgrading and Migrating SystemLink Server

Upgrading to a new version or migrating between SystemLink Servers is a common practice for many deployments. These processes can create risk, and the goal of this chapter is to prepare system administrators to complete this operation in the lowest risk manner possible. A constant throughout this process should be to retain a fully operable SystemLink Server in cases of issues during an upgrade or migration.

!!!important
    It is recommended to run SystemLink Server, attached file stores, and databases as virtual machines. Virtual machines simplify the creation of backups. The use of other tools to facilitate the backup of bare metal (non-virtual machines) is outside the scope of this chapter.

## Assumptions and Prerequisites

- A server running SystemLink 2021 R1 or greater.
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
    - Removable storage volumes or devices

## Preparing for Upgrade or Migration

A constant throughout this document is the capability to backup your server, file stores, and databases. Prior to attempting any upgrade or migration you should backup these components. Failure to create backup increases the risk of unplanned downtime in the case of issues during the upgrade or migration.

!!!note
    **Single node** refers to the SystemLink Server configuration where the application server, file storage, and databases using by SystemLink are all installed on the same Windows server. This is the default installation for SystemLink Server.

    **Multi node** refers to configurations where the file store or data bases used by SystemLink are running on distinct hardware from the SystemLink application server. This is the recommended configuration for all production deployments.

### NI-SystemLink-Migration Command Line Utility

The workflows for upgrades and migration make use of the SystemLink command line migration tool, `nislmigrate`. Refer to the readme at the [NI-SystemLink-Migration](https://github.com/ni/NI-SystemLink-Migration) GitHub repo for details on installing and using this tool.

!!!note
    `nislmigrate` supports capturing data from individual services as well as all installed services using the `--all` parameter. For brevity `--all` is used in the workflows for recommended patterns for upgrading and migrating your SystemLink server. Depending on your needs you may replace the `--all` parameter is one or more of the individual service parameters.

## Recommended Upgrade and Migrations Patterns for your deployment

This chapter will recommend workflows for the following upgrade and migration scenarios. In all scenarios you should plan for some downtime of your SystemLink Server, but by following these recommendations you should minimize this planned downtime.

!!!note
    For upgrades and migrations for a SystemLink Server with a small amount of data you may be able to use `nislmigrate` to backup your data to the local file system of your SystemLink Server. For SystemLink Servers with a large amount of data be aware `nislmigrate` could exhaust the local storage on the server. This can mitigated by using an attached volume. **This document will refer to this attached volume as `D:\` in each pattern.**

- [Single node upgrade](#single-node-upgrade)
- [Single node to multi node migration](#single-node-to-multi-node-migration)
    - [Multi node with MongoDB](#multi-node-with-mongodb)
    - [Multi node with Remote File Store](#multi-node-with-remote-file-store)
- [Multi node upgrade](#multi-node-upgrade)
- [Seamless cut-over](#seamless-cut-over)

## Single Node Upgrade

The NI Package Manager Installers (NIPM) supports in-place upgrade of SystemLink Server. In this case, an in place upgrade is one where the upgrade is run directly on your current SystemLink Server. For production deployments of SystemLink Server this is not recommended. If you pursue this option it is highly recommended you backup your server prior to the upgrade. This backup is an essential fallback should an issue occur during upgrade that leaves your SystemLink in a bad state.

For single node upgrades, NI recommends pairing the upgrade with a migration. This mitigates risks of issues during the upgrade by ensuring your original SystemLink Server remains in an operable state.

1. Backup your SystemLink Server.

1. Attach a volume to store data captured by `nislmigrate`. This will be referred to as `D:\`.

1. Install `nislmigrate`.

1. Run the command `nislmigrate capture --all --secret <your secret> --dir D:\migration`.

    !!!note
        while `nislmigrate` runs all SystemLink services are stopped. Plan ahead for this downtime of your SystemLink server. When the capture is completed, SystemLink services will be restarted automatically.

1. Detach `D:\`.

    !!!note
        At this point in the workflow your original SystemLink Server is in an operable state. Be aware if any new data is created or ingested by the SystemLink server at this time it will not be available to your new server.

1. Provision a new Window server for SystemLink.

1. Install and configure the new version of SystemLink Server.

1. Install `nislmigrate` on your new SystemLink Server.

1. Attach the `D:\` volume used to capture data from your original SystemLink server.

1. Run the command `nislmigrate restore --all --secret <your secret> --dir D:\migration`

1. Verify your new SystemLink Server has all the expected migrated data.

## Single node to Multi Node Migration

In this section two scenarios are described to highlight steps needed when using a dedicated MongoDB server or replicate set and dedicated remote file storage such as an SAN or AWS S3. For clarity each workflow is described separately, but they can be combined if your SystemLink Server is configured to use both types of these remote data stores.

### Multi node with MongoDB

1. Backup your SystemLink Server.

1. Attach a volume to store data captured by `nislmigrate`. This will be referred to as `D:\`.

1. Install `nislmigrate`.

1. Run the command `nislmigrate capture --all --secret <your secret> --dir D:\migration`.

1. Detach `D:\`.

    !!!note
        At this point in the workflow your original SystemLink Server is in an operable state. Be aware if any new data is created or ingested by the SystemLink server at this time it will not be available to your new server.

1. Provision a new Window server for SystemLink.

1. Provision a new MongoDB server or replica set.

1. Install and configure the same or a newer version of SystemLink Server.

    !!!note
        This step prescribes using a newly created instance of your MongoDB server or replica set. This is because SystemLink may change the internal scheme of collections within MongoDB. If you do not start with a instance form back and this occurs you will be unable to revert the MongoDB collections into the schema needed for the older version of SystemLink.

1. Configure SystemLink to use the newly created MongoDB server or replica set.

1. Install `nislmigrate` on your new SystemLink Server.

1. Attach the `D:\` volume used to capture data from your original SystemLink server.

1. Run the command `nislmigrate restore --all --secret <your secret> --dir D:\migration`

1. Verify your new SystemLink Server has all the expected migrated data.

### Multi node with Remote File Store

Its recommended to use a dedicate file store for SystemLink it mitigate the possibility of exhausting the SystemLink Servers local storage. The following workflow describes how to migrate locally stored files to a dedicated remote file store.

TODO pending feature for in place migration.
TODO what about the case where you only need to migrate file meta data.

### Migrating to Multi node to use PostGreSQL for Test Monitor

As of SystemLink 21.5.TODO VERSION NUMBER SystemLink supports using PostGreSQL as the database backing the Test Monitor Service. This configuration is optional, but provides significant performance improvements. `nislmigrate` does not yet support migrating PostGreSQL directly.

The Test Monitor Service itself performs the migration of test steps, test results, and product from MongoDB to PostGreSQL. If you intend on utilizing a single node configuration the steps for this migration are the same as described in [**Single Node Migration**](#single-node-migration). Use the following workflow if you intend on migrating or upgrading to a new server and utilize a multi node configuration where PostGreSQL is hosting on a dedicated server or replica set.

1. Backup your SystemLink Server.

1. Attach a volume to store data captured by `nislmigrate`. This will be referred to as `D:\`.

1. Install `nislmigrate`.

1. Run the command `nislmigrate capture --all --secret <your secret> --dir D:\migration`.

1. Detach `D:\`.

    !!!note
        At this point in the workflow your original SystemLink Server is in an operable state. Be aware if any new data is created or ingested by the SystemLink server at this time it will not be available to your new server.

1. Provision a new Windows server for SystemLink.

1. Provision a PostGres server or replica set.

1. Install and configure the new version of SystemLink Server that supports PostGreSQL

    !!!note
        If you are using the single node configuration for SystemLink the migration from the local instances of MongoDB to PostGreSQL will begin automatically. If you are in a multi node configuration where a dedicated MongoDB server or replica set is used, you must specify the PostGreSQL instance for SystemLink to use before the MongoDB to PostGreSQL migration can occur. The next step in this workflow assumes you are in this multi node configuration.

1. Configure SystemLink to use the newly created PostGreSQL server or replica set and click **Save**. Refer to [Connecting to a Remote PostgreSQL Database](https://www.ni.com/documentation/en/systemlink/latest/setup/remote-postgres-databse/) for this step.

1. Install `nislmigrate` on your new SystemLink Server.

1. Attach the `D:\` volume used to capture data from your original SystemLink server.

1. Run the command `nislmigrate restore --all --secret <your secret> --dir D:\migration`

    !!!note
        After this step SystemLink will migrate your test steps, results, and products from MongoDB to PostGreSQL. Depending on the size of your data set this process may take some time.

1. Verify your new SystemLink Server has all the expected migrated data.

### Upgrading Multi node configurations (MongoDB, PostGreSQL, File Share/S3)

The following workflow describes upgrading a SystemLink server that has been configured to use a dedicated MongoDB server or replica set, a dedicated PostGreSQL server or replica set, and a dedicated file store such as AWS S3.

1. Backup your SystemLink Server, MongoDB server or replica set, PostGreSQL replica set, and file store.

    !!!note
        If S3 is used as your file store the backup step is not needed since this managed internally to AWS S3.

1. Attach a volume to store data captured by `nislmigrate`. This will be referred to as `D:\`.

1. Install `nislmigrate`.

1. Run the command `nislmigrate capture --tags --dir D:\migration`.

1. Detach `D:\`.

    !!!note
        At this point in the workflow your original SystemLink Server is in an operable state. Be aware if any new data is created or ingested by the SystemLink server at this time it will not be available to your new server.

1. Provision a new Windows server for SystemLink.

1. Provision a MongoDB server or replica set from the backup previously created.

1. Provision a PostGres server or replica set from the backup previously created.

1. Install and configure the new version of SystemLink Server.

1. Configure SystemLink to use the newly created MongoDB server or replica, PostGreSQL server or replica set, and existing file store.

1. Install `nislmigrate` on your new SystemLink Server.

1. Attach the `D:\` volume used to capture data from your original SystemLink server.

1. Run the command `nislmigrate restore --tags`.

1. Verify your new SystemLink Server has all the expected migrated data.

## Seamless Cut-over

Since managed test systems are connected SystemLink it is desirable to managed upgrades and migrations such that test systems can connect to the new instance of SystemLink without additional manual intervention. To accomplish this the following conditions must be met.

- Migration of systems data. This is either accomplished by using the `nislmigrate` parameters `--all` or `--systems` or by connecting with a MongoDB server or replica set that contains systems data.

- The DNS name of the original SystemLink Server and the new SystemLink Server are the same.

- If NI Web Server has been configured for HTTPS, the new SystemLink Server must use the same TSL certificate as the original SystemLink Server.
