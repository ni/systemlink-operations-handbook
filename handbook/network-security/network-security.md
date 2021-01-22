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
    - File, tag, test, and asset data are published to the SystemLink app server over `https`.
        - Refer to [**Web Server and TLS**](#web-server-and-tls) for details on configuring encrypted communication.

- **MongoDB**
    - MongoDB is the primary database used by SystemLink's web services and the [MongoDB wire protocol](https://docs.mongodb.com/manual/reference/mongodb-wire-protocol/) is used to interact with the MongoDB instance.
    - Refer to [TLS for Remote MongoDB Instances](#tls-for-remote-mongodb-instances) for details on secure access and encrypted communication.

- **File Ingestion Service Storage**
    - The File Ingestion Services (FIS) can be configured to store files on either Network Attached Storage (NAS) or AWS S3.
    - NAS uses the `smb` protocol. TODO make sure you aren't describing something that is not NAS
    - AWS S3 uses `https`.
    - TODO can we use Azure blob storage like NAS??????
    - Make 

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

NI Web Server is based on [**Apache httpd***](https://httpd.apache.org) and includes the **NI Web Server Configuration** utility assisting users with choosing secure presets as well as a GUI for making changes to the various `.conf` files used by Apache httpd.

!!! note
    NI Web Server ships with SystemLink and various other NI software products such as LabVIEW.

    Refer to the [NI Web Server manual](https://www.ni.com/documentation/en/ni-web-server/latest/manual/manual-overview/) for step by step instructions to configure your web server. The following provides details on the security features exposed by **NI Web Server Configuration**.

### HTTPS

TODO check version of TLS

**NI Web Server Configuration** supports creating self-signed certificates, certificate signing requests (CSR), and installing certificates generated by a certificate authority. The DNS settings for the server can affect the operability of these certificates. Refer to [**DNS Configuration**](#dns-configuration) for details.

!!! note "Limited capabilities when using self-signed certs"

    When using a self-signed cert clients will not trust the cert by default. This can prevent certain operations from occurring.

    - Health tags from targets will not automatically publish

    - Test results from the [NI SystemLink Test Monitor Client plugin](https://www.ni.com/documentation/en/systemlink/latest/tests/integrating-with-teststand/) will not be published and the error XXXX will be returned in the TestStand UI.

    - Packages built in LabVIEW cannot be [automatically published](https://www.ni.com/documentation/en/systemlink/latest/deployment/creating-packages-labview-package-builder/) to SystemLink server.

    - The LabVIEW Client API will have to explicitly disable verify server checks to communicate with the server.
        - Refer to [Open Configuration ](https://www.ni.com/documentation/en/systemlink/latest/systemlink-labview-node-ref/open-configuration-http-auto/) to details on this setting.

When you have received a certificate from an certificate signing authority, you can use **NI Web Server Configuration** to install the certificate.

1. Open **NI WEb Sever Configuration** and navigate to the **HTTPS** tab.

2. Click the **Use a certificate from a signing authority** radio button.

3. Expand the **Install an already signed certificate** section.

4. Click the folder icon next to **Certificate file** and browse to your certificate file.

5. Click the folder icon next to **Key file** and select your key file.

6. If needed change the HTTPS port from the default, 443.

7. Click **Apply and restart**.

!!! note "Intermediary signing authorities"

    TODO look up the corner case here. 

### DNS Configuration

SystemLink and NI Web Server do not ship with a DNS server. The following assumes a production DNS server is available in your environment. NI Web Server will attempt to provide a default for the DNS of your SystemLink server based on Windows OS settings. Other potentially valid DNS names are listed in the **Preferred host name for generated URLs and certificates** combo box. You may also manually enter another host name as needed. As the name of the combo box implies, this setting must match the host name that will be used for TLS certificates. This hostname is also sent to systems managed by SystemLink to inform them of the host name of the server. If an invalid hostname is provided data from managed systems will not be published.

### CORS and Remote Connections

In ideal scenarios CORS can be disabled to achieve a higher degree of security. In practice, CORS may need to be enabled to facilitate workflows for users developing web applications that interact with SystemLink's API. For this scenario, NI recommends setting up a *test* SystemLink server with looser CORS settings, such that your *production* SystemLink server can restrict CORS completely.

The settings for choosing a remote connection assist with setting Windows Firewall rules to ensure connections may only be established by clients on your preferred network.

Refer to [Choosing Remote Settings](https://www.ni.com/documentation/en/ni-web-server/latest/manual/choosing-a-remote-setting/) for details on the various CORS and remote connection settings.

TODO considerations for official certs and intermediary authorities
TODO what happens if you are using self-signed certs and how to manually copy these other (not recommended)

### Test System to SystemLink communication

Test Systems communicate with SystemLink over HTTP(S) and SaltStacks TCP protocol. Refer to [**HTTPS**](#https) for details on enabling HTTPS in NI Web Server.

Link to workflows for establishing a secure connection from target to server.

Per the target changing masters Josh says:
        The recommendation is that the customer sets a password on the target.  The person taking the system is required to enter the targets password.  In addition, we also show the current master when adding a system to confirm the user wants to take it.
        We show a warning in the UI for any RT system without a password.
        The password would also be required by anyone trying to use MAX to change the master.
 like 1
    Without the password anyone can ssh into the box with  `admin` and no password

Registration and credential transfer - Link to VI/API documentation on auto here

Double check if we are really automatically deploying Self signed certs to targets. I thought we just had only trust signed certs.

### Communication with SystemLink web application

## TLS for SaltStack

TODO Discussion of how this cert is setup and configured

## TLS for remote MongoDB Instances

## TLS for remote file storage

TODO mention that repository files are always stored locally.

### Using Network Attached Storage

### Using Amazon S3

## Deprecation of AMQP

TODO discussion of AMQP deprecation, why we did this, and workspaces.

Put in details about how to disable remote AMQP access