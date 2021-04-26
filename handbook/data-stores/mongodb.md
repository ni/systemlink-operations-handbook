# MongoDB

The majority of SystemLink services use [MongoDB](https://www.mongodb.com) as the primary datastore. Default installations of SystemLink include MongoDB community Edition and launch it when the SystemLink server boots. This is referred to as a [*single node*](#single-node-deployments) deployment.

You can slo host MongoDB on a separate stand-alone server, a [replica set](https://docs.mongodb.com/manual/replication/) of 3 or more servers, or accessed through MongoDB's Platform as a service offering: [MongoDB Atlas](https://www.mongodb.com/cloud/atlas). This is referred to as a [*multi node*](#multi-node-deployments) deployment.

## Assumptions and Prerequisites

Before you configure a remote MongoDB to use with SystemLink, ensure you have the following:

- A server running SystemLink 2021R1 or greater. Refer to [Installing and Configuring SystemLink Server and Clients](https://www.ni.com/documentation/en/systemlink/latest/setup/configuring-systemlink-server-clients/) for the basics of setting up a SystemLink server.
- A standalone server running MongoDB, multiple servers hosting a MongoDB replica set, or a MongoDB Atlas Account
- A user with the `readWriteAnyDatabase` or similar role. Refer to [Role-Based Access Control](https://docs.mongodb.com/manual/core/authorization/) for details.

## Single Node vs Multi Node MongoDB Deployments

The following table summarizes when to consider the various supported configurations of MongoDB with SystemLink.

| Diagram | SystemLink + MongoDB Configuration | When to use |
| | ----------- | ----------- |
|<img src="../../img/single-box.png" width="1500px"/>| Single node with Defaults     | You have one server hosting both MongoDB and SystemLink. Use this during evaluation, when working with less than 10 managed nodes, and in deployments that don't need the Asset Manager and Test Insights modules.
|<img src="../../img/single-box.png" width="1500px"/>| Single node with increased index cache   | You have one server hosting both MongoDB and SystemLink. Use this during evaluation, in moderate deployments of less than 25 managed nodes, and moderate usage of the Test Insights module producing less than 100 test steps and results each day.  |
|<img src="../../img/mdb-sa.png" width="1500px" />| Multi node with single standalone MongoDB Instance | You have SystemLink and MongoDB are hosted on two separate servers. Use when the CPU, memory, and disk consumption of the MongoDB service is impacting the operation of SystemLink services. Note, while this configuration provides for greater reliability by splitting the servers running SystemLink and MongoDB, it does not provide greater redundancy for data storage.   |
|<img src="../../img/mdb-rs.png" width="1500px"/>| Multi node with MongoDB replica sets | You have SystemLink hosted on a dedicated server and MongoDB hosted on 3 or more servers. **This is the recommended configuration for all production deployments including small and moderately sized deployments.** Use this to enable greater scale (>50 managed nodes, >1000 test steps and results daily). This configuration mitigates data loss with redundant replica sets. Refer to [MongoDB documentation](https://docs.mongodb.com/manual/tutorial/deploy-replica-set/) for setting up and hosting a MongoDB instance with replica sets. |
|<img src="../../img/mdb-atlas.png" width="1500px"/>| Multi node with MongoDB Atlas | You have SystemLink hosted on a dedicated server and connect to a MongoDB Atlas cluster. Use for large scale deployments (>200 managed node, 10,000 test steps and results daily). MongoDB Atlas also simplifies database provisioning, operation, backup and restore. These features may be desireable at any scale of deployment. Refer to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) for details on this service.

## Single Node Deployments

By default, SystemLink stores all data in databases and the file system hosted on the SystemLink application server. For more reliable data storage and scalability, Ni recommends remote data stores for all production deployments.

### Increasing the index cache size for *single node* deployments

Increase the index cache size to process more data and use the Test Insights or Asset Management modules in a single-node deployment. This avoids high CPU usage that can occur with the default MongoDB memory constraints in SystemLink. NI recommends increasing the available memory for the index to 8GB. Refer to [Sizing a SystemLink Server](https://www.ni.com/documentation/en/systemlink/latest/setup/sizing-a-systemlink-server/) for system requirements to run SystemLink.
  
1. With a user with administrator privileges, log into the desktop of the SystemLink app server.
1. Open **NI SystemLink Server Configuration**.
1. Navigate to **NoSqlDatabase**.
1. Under **The NoSqlServer is launched and managed by SystemLink**, adjust the value in **The cache size of the database in Gigabytes (GB)**.
1. Click **Apply**.

!!!note
    Refer to [Sizing a SystemLink server](https://www.ni.com/documentation/en/systemlink/latest/setup/sizing-a-systemlink-server/) for guidance on the CPU, memory, and disk needed for SystemLink single node deployments.

## Multi Node Deployments

SystemLink supports three types of multi-node configuration. You can configure SystemLink to connect to a standalone instance, replica sets, or MongoDB Atlas.

NI recommends connecting SystemLink to replica set of three or more MongoDB servers for all production deployments.

!!!important
    Due to a bug in a 3rd party MongoDB driver, SystemLink cannot connect to MongoDB instances where the MongoDB username provided in the form input or connection string contains either the `-` or the `_` character.

- NI does not support configurations where multiple SystemLink servers use the same MongoDB instance.
- NI does not support configurations where another production application uses the same MongoDB instance as SystemLink.

!!!note
    While SystemLink can connect to and use a sharded MongoDB cluster (`mongos`), it will not take advantage of horizontal scaling capabilities enabled by sharded clusters.

When using a stand-alone MongoDB instance, replica set, or Atlas, you have the option to encrypt the data stored within the database. This is built into MongoDB Atlas or requires [MongoDB Enterprise Advanced](https://www.mongodb.com/products/mongodb-enterprise-advanced) for stand-alone or replica sets.

!!!important "Connection String Formats"
    Some connection string formats are unsupported or could cause issues in some environments.

    - Connection strings that contain the query parameter `tls=` are unsupported. Use the `ssl=` query string to achieve the same capability with the same degree of security.
    - In environments where the 4.2.1.1 root DNS server cannot be reached, the DNS seed list URI format (`mongodb+srv://`) will fail due to a bug ([Unable to connect to Atlas due to DNS connectivity issues #358](https://github.com/kobil-systems/mongodb/issues/358)) in a 3rd party MongoDB driver used by SystemLink. In this case use the [MongoDB standard connection string format](https://docs.mongodb.com/manual/reference/connection-string/#std-label-connections-standard-connection-string-format) to connect your replica set. This affects both self-hosted replica sets and MongoDB Atlas.
    - When URL escaping characters in your connection string  you must use uppercase characters, e.g. `%2F` not `%2f`.

    Example connection string (line breaks for readability):
    
    ```url
    mongodb://myusername:<password>@
    ec2-123-123-12.compute-1.amazonaws.com27017,
    ec2-234-234-23.compute-1.amazonaws.com:27017,
    ec2-456-456-45.compute-1.amazonaws.com:27017/
    ?authSource=admin
    &replicaSet=rs0
    &readPreference=primary
    &ssl=true
    ```

    Consider using [MongoDB Compass](mongodb compass) to connect to your replica set to help construct a valid connection string and verify the configuration.

### Connecting to Standalone MongoDB instance

Using a separate server to host MongoDB increases reliability and lowers resource utilization for your SystemLink server.

You may use the supplied form input in **NI SystemLink Sever Configuration** when connecting to a server hosting a single standalone MongoDB instance. Refer to [Connecting to a Remote Mongo Database](https://www.ni.com/documentation/en/systemlink/latest/setup/remote-mongo-database/) for more information.

### Connecting to MongoDB with Replica Sets

Replica sets provide a way to create redundancy in your database to mitigate against potential data loss from the loss of a server hosting MongoDB. Refer to MongoDB for a [tutorial on deploying replica sets](https://docs.mongodb.com/manual/tutorial/deploy-replica-set/).

To successfully connect to a MongoDB replica set and create redundancy, you must specify a connection string in **NI SystemLink Server Configuration**.

!!! note
    NI recommends [x.509 certificates](https://docs.mongodb.com/manual/tutorial/configure-x509-member-authentication/) for replica set membership.

1. Log into the desktop of the SystemLink app server with administrator privileges
1. Open **NI SystemLink Server Configuration**.
1. Navigate to **NoSqlDataBase**.
1. Click the **Connect to an externally managed NoSqlDatabase server** radio button.

    !!!note "Secure remote connections"
        NI recommends securing communications between your SystemLink server and MongoDB instance with TLS. For details, refer to [TLS for Remote MongoDB Instances](/network-security/network-security/#tls-for-remote-mongodb-instances).

1. Select the **Use a custom connection string** checkbox.
1. Enter your connection string. [Refer to Connection String URI Format](https://docs.mongodb.com/manual/reference/connection-string/) for details on structuring your connection string.
1. Click **Test Connection** to ensure SystemLink can connect to the MongoDB instance.
1. If the connection test was successful, click **Apply** to restart SystemLink service manager and connect to the MongoDB instance.

<figure>
  <img src="../../img/mdb-cache.png" width="500" />
  <figcaption>SystemLink's NoSqlDatabase configuration set to 8BG</figcaption>
</figure>

### Connecting to MongoDB Atlas

Connect to MongoDB Atlas for simpler setup and adminstration of a MongoDB replica set compared to self hosting. MongoDB Atlas is a fully managed PaaS from MongoDB.

If you have not setup an Atlas cluster before, refer to [Getting started with Atlas](https://docs.atlas.mongodb.com/getting-started/). Refer to [Setup Atlas Connectivity](https://docs.mongodb.com/guides/cloud/connectionstring/) for steps to obtain a connection string.

!!! note
    In the sample connection string provided by Atlas you will need to replace the instance of `myFirstDatabase` with `admin`. For example:

    ```url
    mongodb+srv://<username>:<password>@<cluster>/myFirstDatabase?retryWrites=true&w=majority
    ```
    
    This will need to be updated to 
    
    ```url
    mongodb+srv://<username>:<password>@<cluster>/admin?retryWrites=true&w=majority
    ```

!!!important "MongoDB Atlas free tier is unsupported by SystemLink"
    Due to constraints on memory in the Atlas free tier, you must use a paid tier for SystemLink to successfully connect. SystemLink supports all paid tiers for Atlas. If you need assistance evaluating Atlas with SystemLink please contact NI ([customer.requests@ni.com](mailto:customer.requests@ni.com)) or your local account manager.

Because Atlas uses replica sets by default, your SystemLink server could be affected by the bug in the 3rd party MongoDB driver used by SystemLink as described in [Multi Node Deployments](#multi-node-deployments). When obtaining a connection string from Atlas use the connection string generated for the Node.js driver version 2.0.14. This provided connection string is fully supported by SystemLink.
