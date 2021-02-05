# Network Security

SystemLink connects test systems to a central server to aggregate data for monitoring and analysis. SystemLink uses standard tools and industry best practices to ensure the SystemLink server and test systems utilize secure networking techniques.

Refer to [Workspaces and Role-based Access Control](/rbac/rbac) for details users securely interact with SystemLink resources. Refer to [Single Sign-on with OpenID Connect](/openid-connect/openid-connect/) and [Sign on with LDAP](/ldap/ldap/) for details on security authenticating with SystemLink.

For brevity **HTTPS** is referenced for scenarios where HTTPS or HTTP could be used. NI recommends HTTPS for production.

## Network diagram

<figure>
  <img src="../../img/network-diagram.png" width="500" />
  <figcaption>The components and TLS protocols used by SystemLink.</figcaption>
</figure>

The above network diagram summarizes connections with the following components. Refer to [Setting up a SystemLink Server](https://www.ni.com/documentation/en/systemlink/2020r4/setup/setting-up-systemlink-server/) for information regarding ports used by SystemLink. TLS protocols are shown where available.

- **SystemLink App Server**:
    - This Windows server hosts NI Web Server, the various SystemLink services, and SystemLink web applications.
    - In the *single-box* setup, MongoDB and FIS storage are hosted on the app server.
    - Refer to [Sizing a SystemLink Server](https://www.ni.com/documentation/en/systemlink/2020r4/setup/sizing-a-systemlink-server/) for details on server system requirements.
    - NI assumes users with desktop access to the server are outside of the security controls and capabilities described by this document. Securing desktop access to the SystemLink app server should be managed by the customer's IT security protocols.

- **SystemLink Web app**
    - The SystemLink web application is the primary way users interact with SystemLink.
     `https` or `https` is used to communicate with the web application.
    - Refer to [**Web Server and TLS**](#web-server-and-tls) for details on configuring encrypted communication.

- **Testers**
    - Testers are systems who software and configuration are managed by SystemLink.
    - Software configuration occurs via the [SaltStack Transport Protocol](https://docs.saltproject.io/en/latest/topics/transports/).
        - Refer to [**TLS for SaltStack**](#tls-for-saltstack) for details regarding how SystemLink encrypts this communication.
        - Refer to [Hardening Salt](https://docs.saltproject.io/en/latest/topics/hardening.htmlteam ) for additional resources on securing this capability in SystemLink.
    - File, tag, test, and asset data are published to the SystemLink app server over `https`.
        - Refer to [**Web Server and TLS**](#web-server-and-tls) for details on configuring encrypted communication.

- **MongoDB**
    - MongoDB is the primary database used by SystemLink's web services and the [MongoDB wire protocol](https://docs.mongodb.com/manual/reference/mongodb-wire-protocol/) is used to interact with the MongoDB instance.
    - Refer to [TLS for Remote MongoDB Instances](#tls-for-remote-mongodb-instances) for details on secure access and encrypted communication.

- **File Ingestion Service Storage**
    - The File Ingestion Services (FIS) can be configured to store files on either Network Attached Storage (NAS) or AWS S3.
    - NAS uses the `smb` protocol.
        - The SMB protocol can be configured to use AES encryption. Refer to [SMB security enhancements](https://docs.microsoft.com/en-us/windows-server/storage/file-server/smb-security) for details and steps to secure this transport.
    - AWS S3 uses `https`.
        Refer to the [SystemLink manual](https://www.ni.com/documentation/en/systemlink/latest/data/uploading-files-to-amazon-s3/) for steps to enable S3 file storage.

- **Data Finder**
    - DataFinder enables indexing and searching for files stored on network drives.
    - DataFinder's network communication cannot be secured with TLS.

- **Identity Provider**
    - Active Directory, LDAP, and OpenID Connect are the supported identity providers.
        - Local Windows account may also be used (not shown)
        - Active Directory used the Active Directory protocol.
        - LDAP uses the `ldap` or the `ldaps` protocols.
        - OpenID Connect uses `https` or `https`.
    - Refer to [Sign-on with LDAP](/ldap/ldap/). and [Single Sign-on with OpenID Connect](/openid-connect/openid-connect/) for details on using these identity providers.

- **NI VLM**
    - NI Volume License Manager (VLM) is used to enforce SystemLink node licenses.
    - NI VLM uses TCP and does not support TLS.
    - Refer to [Licensing SystemLink Products](https://www.ni.com/documentation/en/systemlink/2020r4/setup/licensing-systemlink/) for details on using VLM with SystemLink.

## NI Web Server

NI Web Server is based on [**Apache httpd***](https://httpd.apache.org) and includes the **NI Web Server Configuration** utility to aid users to choose a secure presets as well as a GUI for changing the Apache httpd configuration.

!!! note
    NI Web Server ships with SystemLink and various other NI software products such as LabVIEW.

    Refer to the [NI Web Server manual](https://www.ni.com/documentation/en/ni-web-server/latest/manual/manual-overview/) for step by step instructions to configure your web server. The following provides details on the security features exposed by **NI Web Server Configuration**.

### Using HTTPS in NI Web Server

NI Web Server supports TLS 1.2.

**NI Web Server Configuration** supports creating self-signed certificates, certificate signing requests (CSR), and installing certificates generated by a certificate authority. The DNS settings for the server can affect the operability of these certificates. Refer to [**DNS Configuration**](#dns-configuration) for details. Self signed certificates should be used for testing purposes only.

!!! note "Limited capabilities when using self-signed certs"

    When using a self-signed cert clients will not trust the cert by default. This can prevent certain operations from occurring.

    - Web browsers will not trust the certificate and the user must grant an exception to load the SystemLink web application.

    - Packages built in LabVIEW cannot be [automatically published](https://www.ni.com/documentation/en/systemlink/latest/deployment/creating-packages-labview-package-builder/) to SystemLink server.

    - The LabVIEW Client API will have to explicitly disable verify server checks to communicate with the server.
        - Refer to [Open Configuration ](https://www.ni.com/documentation/en/systemlink/latest/systemlink-labview-node-ref/open-configuration-http-auto/) to details on this setting.

When you have received a certificate from an certificate signing authority, you can use **NI Web Server Configuration** to install the certificate.

1. Open **NI Web Sever Configuration** and navigate to the **HTTPS** tab.

2. Click the **Use a certificate from a signing authority** radio button.

3. Expand the **Install an already signed certificate** section.

4. Click the folder icon next to **Certificate file** and browse to your certificate file.

5. Click the folder icon next to **Key file** and select your key file.

6. If needed change the HTTPS port from the default, 443.

7. Click **Apply and restart**.

!!! note "TLS Certificates with application load balancers"
    If you have a load balancer in front of your SystemLink app server you must ensure the same certificate is installed on both the load balancer and NI Web Server for a tester to successfully connect and publish data to SystemLink.

### DNS Configuration

SystemLink and NI Web Server do not ship with a DNS server. The following assumes a production DNS server is available in your environment. NI Web Server will attempt to provide a default for the DNS of your SystemLink server based on Windows OS settings. Other potentially valid DNS names are listed in the **Preferred host name for generated URLs and certificates** combo box. You may also manually enter another host name as needed. As the name of the combo box implies, this setting must match the host name that will be used for TLS certificates. This hostname is also sent to systems managed by SystemLink to inform them of the host name of the server. If an invalid hostname is provided data from managed systems will not be published.

### CORS and Remote Connections

In ideal scenarios CORS can be disabled to achieve a higher degree of security. In practice, CORS may need to be enabled to facilitate workflows for users developing web applications that interact with SystemLink's API. For this scenario, NI recommends setting up a *test* SystemLink server with looser CORS settings, such that your *production* SystemLink server can restrict CORS completely.

The settings for choosing a remote connection assist with setting Windows Firewall rules to ensure connections may only be established by clients on your preferred network.

Refer to [Choosing Remote Settings](https://www.ni.com/documentation/en/ni-web-server/latest/manual/choosing-a-remote-setting/) for details on the various CORS and remote connection settings.

### Test System to SystemLink communication

Test Systems communicate with SystemLink over HTTP(S) and SaltStacks TCP protocol. Refer to the SystemLink manual for prerequisites and steps to add a [Linux RT target]((https://www.ni.com/documentation/en/systemlink/latest/setup/setting-up-systemlink-client-linux/)) or [Windows target](https://www.ni.com/documentation/en/systemlink/latest/setup/setting-up-systemlink-client-windows/) to your SystemLink server.

Data published over HTTPS includes tags, files (FIS), assets, and test results. Salt jobs and Salt pillars communicate over the AES encrypted Salt TCP transport. Salt jobs are used for installing software and changing target configuration from SystemLink server. Salt pillars are used to transfer credentials and certificates. The certificates used on the SystemLink server and target nodes are managed by Salt and does not require administrators to externally manage these certificates. Refer to SaltStack's [documentation](https://docs.saltproject.io/en/getstarted/system/communication.html) for an overview of the Salt TCP Transport.

!!! note "Managed NI LinuxRT Nodes"
    NI recommendations setting a username and a password on the node. These credentials are required to SSH into the node. These credentials are required when a SystemLink server adds the Linux RT client to its collection of managed systems.

When a target is approved by SystemLink and becomes a managed node, SystemLink securely transfers configuration, certificates, and credentials needed to authenticate with the SystemLink server's [role-based access control system](/rbac/rbac/). SystemLink client APIs include an [**Auto** configuration](https://www.ni.com/documentation/en/systemlink/latest/systemlink-labview-node-ref/open-configuration-http-auto/) that uses the credentials automatically. This prevents the need to include credentials and other secrets in your test application code.

!!! warn "Do not expose Salt ports to the public internet"

    Due to the capabilities of Salt, users are encourage to configure firewalls and appropriate CIDR blocks to prevent access to the Salt ports (4505 and 4506) to the public internet.

## TLS for remote MongoDB Instances

MongoDB support TLS connections. Refer to the [MongoDB manual](https://docs.mongodb.com/manual/tutorial/configure-ssl/) for details on enabling TLS. NI recommends enabling TLS for remote MongoDB connections. I

!!! note

    SystemLink does not support `mongod` instances configured for Client Certificate validation. Ensure `mongod` is started without this requirements to allow SystemLink to successfully connect.

### Connecting to `mongod` Using Self-signed Certificates

Self signed certificates should be used for testing purposes only. If you are using a self signed certificate on your `mongod` instance you must install the CA certificate and intermediary certificate into the SystemLink app server. Refer, to the [MongoDB manual](https://docs.mongodb.com/manual/appendix/security/appendixA-openssl-ca/) for steps to create and run `mongod` with a self-signed certificate.

!!! note "Running `mongod` without Client certificate validation"

    With command line arguments:
    ```bash
    mongod --tlsMode requireTLS --tlsCertificateKeyFile /etc/ssl/test-server1.pem --port 27017 --dbpath /var/lib/mongo --bind_ip_all
    ```

    With a Mongo Configuration file:
    ```yaml
    net:
        port: 27017
        bindIp: 0.0.0.0
        tls:
            mode: requireTLS
            certificateKeyFile: /etc/ssl/test-server1.pem
    systemLog:
        destination: file
        logAppend: true
        path: /var/log/mongodb/mongod.log
    storage:
        dbPath: /var/lib/mongo
        journal:
            enabled: true
    processManagement:
        fork: true  #fork and run in background
        pidFilePath: /var/run/mongodb/mongod.pid  # location of pidfile
        timeZoneInfo: /usr/share/zoneinfo
    ```

#### Installing MongoDB Self-Signed Certificates

Use the following steps to install the CA and intermediary certificates onto the SystemLink app server.

1. Copy the CA and ia `.crt` files to you SystemLink app server.

2. Double click on the CA certificate and click **Install Certificate...**.

    !!! note
        If you are following the [MongoDB manual appendix](https://docs.mongodb.com/manual/appendix/security/appendixA-openssl-ca/) this file is name `mongodb-test-ca.crt`.

3. In the **Store Location** field select the **Local Machine** radio button and click **Next**.

4. Select the **Place all certificate in the following store** radio button.

5. Click **Browse**, select **Trusted Root Certificate Authorities** and click **OK**

6. Click **Next**, review the settings, and click **Finish** to install the certificate.

7. Double click on the CA certificate and click **Install Certificate...**.

    !!! note
        If you are following the [MongoDB manual appendix](https://docs.mongodb.com/manual/appendix/security/appendixA-openssl-ca/) this file is name `mongodb-test-ia.crt`.

8. In the **Store Location** field select the **Local Machine** radio button and click **Next**.

9. Select the **Place all certificate in the following store** radio button.

10. Click **Browse**, select **Intermediate Certificate Authorities** and click **OK**

11. Click **Next**, review the settings, and click **Finish** to install the certificate.

!!! note
    Ensure you have checked the **Use Transport Layer Security (TLS) encryption** in the **NoSqlDatabase** section of the **SystemLink Server Configuration** application.

## Deprecation of AMQP

AMQP as a transport protocol for target to server communication is deprecated in favor for HTTP. This process will be rolled out over several releases to minimize disruption to clients. NI recommends disabling AMQP on the server and updating test applications to use the HTTP version of SystemLink APIs.

1. Open **NI SystemLink Server Configuration**.

2. Go to **Security**.

3. Uncheck **Enable AMQP client access (less secure).
