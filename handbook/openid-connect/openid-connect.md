# Single Sign-on with OpenID Connect

You can configure SystemLink to use OpenID Connect to authorize users. This enables SystemLink to use a common identity for users across multiple applications. This also means SystemLink leverages corporate single sign-on (SSO) and all its security benefits, such as streamlined login and limiting user credential proliferation. You can use OpenID Connect alongside or as a replacement for LDAP, Active Directory, and local Windows accounts for authentication.

## Assumptions and Prerequisites

- A server running SystemLink 2020R4 or greater. Refer to [Installing and Configuring SystemLink Server and Clients](https://www.ni.com/documentation/en/systemlink/latest/setup/configuring-systemlink-server-clients/) for the basics of setting up a SystemLink server

- A DNS name for the SystemLink server

- SystemLink login with the **Server Administrator** role

- Administrator desktop access to the SystemLink server

- An OpenID Connect Provider server such as [PingFederate](https://www.pingidentity.com/en/software/pingfederate.html), [Azure ADFS](https://docs.microsoft.com/en-us/windows-server/identity/ad-fs/deployment/how-to-connect-fed-azure-adfs), [Okta](https://www.okta.com/openid-connect/), or another [certified provider](https://openid.net/certification/) that has been fully setup and configured for OpenID Connect authentication

## Enabling OpenID Connect in SystemLink

1. Log into the server running SystemLink and go to `C:\Program Files\National Instruments\Shared\Web Server\conf\openidc`.

2. Add the configuration files to SystemLink to connect to your OpenID Connect provider.

    !!! note ""
        For details, refer to [**OpenID Configuration Files in SystemLink Server**](#openid-configuration-files-in-systemlink-server).

3. Open **NI Web Server Configuration**.

4. Go to the **Authentication** tab and enable **Use OpenID Connect (advanced)**.

5. Click **Apply and restart**.

6. Login into the SystemLink web application with a user assigned the [**Server Administrator**](https://www.ni.com/documentation/en/systemlink/latest/setup/predefined-roles/) role.

7. Go to **Security** > **Roles** and click the gear icon in the top right.

8. Add an OpenID Claim mapping for the **Server Administrator** role.

    !!! note ""
        For details, refer to [**Mapping OpenID Connect Claims to SystemLink Workspaces and Roles**](#mapping-openid-connect-claims-to-systemlink-workspaces-and-roles).

9. Log out and log in as an OpenID connect user with a mapping for the **Server Administrator** role and confirm they have the correct privileges.

<figure>
  <img src="../../img/oidc-webserver.png" width="500" />
  <figcaption>Enable OpenID Connect in NI Web Server</figcaption>
</figure>

## OpenID Configuration Files in SystemLink Server

There are three files that you must create to connect your SystemLink server to an OpenID Connect provider: `[provider-dns].conf`, `[provider-dns].client`, and `[provider-dns].provider`. The `[provider-dns]` portion of each filename must be the URL-encoded fully qualified domain name.

Refer to [openid-connect-config](https://github.com/ni/systemlink-operations-handbook/tree/master/examples/openid-connect-config) for examples of each of these files.

!!! note "Example"
    An OpenID provider with the DNS `example.com:9999` would yield files named `example.com%3a9999.conf` , `example.com%3a9999.client`, and `example.com%3a9999.provider`.

These files do not exist for new SystemLink installations. Add each file to `C:\Program Files\National Instruments\Shared\Web Server\conf\openidc`. Restart the NI Web Server to apply changes.

You can configure SystemLink to support multiple OpenID Connect providers simultaneously by creating a `[provider-dns].conf`, `[provider-dns].client`, and `[provider-dns].provider` file for each provider. The user ID in SystemLink must be unique across providers. This ID takes the form `[sub_claim]@issuer`. You can see the ID SystemLink associates with a user in the user details in SystemLink Security.

### SystemLink Login Window Configuration

!!! note ""
    `[provider-dns].conf` describes the scopes SystemLink will request, and the text and icon for the provider login button.

    ```json
    {
      "scope": "openid email profile",
      "ni-attributes": {
        "displayName": "Log in with PingFederate",
        "iconUri": "/login/assets/pf.png"
      }
    }
    ```

In this example the `openid`, `email`, and `profile` scopes are requested. Additional scopes may be requested. Consult your provider's documentation regarding exposing scopes to clients. The `profile` and `email` scopes are required to populate first name, last name, and email fields in the SystemLink user preferences. These are derived from the `given_name`, `family_name`, and `email` claims respectively.

Each scope contains claims you can map to roles within SystemLink workspaces. See [**Mapping OpenID Connect Claims to SystemLink Workspaces and Roles**](#mapping-openid-connect-claims-to-systemlink-workspaces-and-roles) for details.

The `ni-attributes` section determines the text and (optionally) an icon to be shown in the SystemLink login page. The `iconUri` is relative to `htdocs` directory (`C:\Program Files\National Instruments\Shared\Web Server\htdocs`). This icon should be 16x16 px.

<figure>
  <img src="../../img/login-window.png" width="500" />
  <figcaption>SystemLink login windows with SSO login option. An icon has not been set in this example</figcaption>
</figure>

### ClientID and Secret

!!! note ""
    The `[provider-dns].client` file is used by the NI Web Server to authenticate with the provider.

    ```json
    {
      "client_id": "slserver",
      "client_secret": "4vFm89u07xaredactedredactedredactede2tjtsEGQhlLreLVjcyLA0"
    }
    ```

The `client_id` and `client_secret` can be obtained from the provider. Depending on the provider the `client_id` may be user defined.

#### ClientID and Secret Provider Documentation

[PingFederate - Configuring an OAuth Client](https://docs.pingidentity.com/bundle/pingfederate-93/page/roj1564002966901.html)

[Using OAuth 2.0 to Access Google APIs](https://developers.google.com/identity/protocols/oauth2)

[Okta - Find your Application's credentials](https://developer.okta.com/docs/guides/find-your-app-credentials/findcreds/)

[ADFS - Build a server side application using OAuth confidential clients with AD FS 2016 or later](https://docs.microsoft.com/en-us/windows-server/identity/ad-fs/development/enabling-oauth-confidential-clients-with-ad-fs)

### OpenID Configuration and Discovery

The `[provider-dns].provider` file includes the contents of the provider's OpenID Connect configuration. This file tells SystemLink which endpoints the provider exposes that are used during login.

!!! note ""
    You may use curl to create this file. Replace `[provider-dns]` with the DNS of your OpenID Connect Provider.

    ```bash
    curl https://[provider-dns]/.well-known/openid-configuration -o [provider-dns].provider
    ```

### Setting Login Redirect URI

The client configuration for your provider requires a redirect URL that is used during the login flow. This must be the fully qualified domain name, the protocol (`https://` or `http://`), and the port (if 80 or 443 are not used) of the SystemLink server. If the SystemLink server's DNS changes, update this setting with your provider.

!!! note
    NI recommends the DNS name in the redirect URI match the the preferred hostname set in NI Web Server Configuration on the SystemLink server.

#### The SystemLink login redirect URL

!!! note ""
    Use the following URL to configure your provider:

    ```url
    [protocol]://[systemlink-dns]/login/openidc-redirect

    ```

#### Provider Client Configuration Documentation

[PingFederate - Configure an OAuth client](https://docs.pingidentity.com/bundle/pingfederate-93/page/roj1564002966901.html)

[Google - Using OAuth 2.0 for Web Server Applications](https://developers.google.com/identity/protocols/oauth2/web-server)

[Okta - Understand the callback route](https://developer.okta.com/docs/guides/sign-into-web-app/springboot/define-callback/)

## Supported Signing and Encryption Algorithms

SystemLink supports the following algorithms for ID token signing, ID token key management encryption, and ID token content encryption.

### ID Token Signing Algorithm

- None

- ECDSA Using P256 Curve and SHA-256

- ECDSA Using P384 Curve and SHA-384

- ECDSA Using P521 Curve and SHA-512

- HMAC using SHA-256

- HMAC using SHA-384

- HMAC using SHA-512

- RSA using SHA-256

- RSA using SHA-384

- RSA using SHA-512

- RSASSA-PSS using SHA-256

- RSASSA-PSS using SHA-384

- RSASSA-PSS using SHA-512

### ID Token Key Management Encryption Algorithm

- No encryption

- Direct Encryption with symmetric key

- AES-128 Key Wrap

- AES-192 Key Wrap

- AES-256 Key Wrap

### ID Token Content Encryption Algorithm

- Composite AES-CBC-128 HMAC-SHA-256

- Composite AES-CBC-192 HMAC-SHA-384

- Composite AES-CBC-256 HMAC-SHA-512

## Mapping OpenID Connect Claims to SystemLink Workspaces and Roles

Map OpenID claims to roles and workspaces so users can access systems and data managed by SystemLink. This process is the same as the mapping workflow for LDAP and Active Directory attributes. Refer to [Assigning Users to Roles in a Workspace](https://www.ni.com/documentation/en/systemlink/latest/setup/mapping-roles/) in the SystemLink manual. You can also use claims to create a mapping for the **Server Administrator** role.

### Viewing Claims Returned by a Provider

The OpenID Connect provider determines which scopes and claims clients can access. To see available claims, use the `userinfo_endpoint` hosted by the provider. Use `https://[provider-dns]/.well-known/openid-configuration` to determine the URL of the `userinfo_endpoint`. You will need to obtain a valid bearer token to authenticate and access this endpoint.  

!!! note ""
    Example curl request to return user info. The bearer token has been truncated for readability.
    ```bash
    curl -s https://slsso-runtime.grl-us1.uat.k8s.com/idp/userinfo.openid -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiI...zJVy2oLnrBmXTmpDRm499U4~'|python -m json.tool
    ```

You can also view claims returned by a particular user by modifying the httpd configuration on your SystemLink server.

1. Go to `C:\Program Files\National Instruments\Shared\Web Server\conf\defines.d\` and open `50_mod_auth_openidc-defines.conf` in a text editor.
2. Change the configuration `UnDefine AUTH_OIDC_ENABLE_CLAIM_INFO` to `Define AUTH_OIDC_ENABLE_CLAIM_INFO`.
3. Restart NI Web Server.
4. Go to `[protocol]://[systemlink-dns]/login/openidc-redirect?info=html` or `[protocol]://[systemlink-dns]/login/openidc-redirect?info=json` to view user claims.

!!! note ""
    An example `50_mod_auth_openidc-defines.conf` modified to expose user claims. You must be logged via OpenID Connect to receive data this endpoint.
    ```conf
    #
    # Defined OpenID-Connect configuration for the Windows Apache installation.
    #

    # The name of the JSON map containing metadata about each identity provider.
    Define AUTH_OIDC_ATTRIBUTES_KEY ni-attributes

    # CA bundle to use when making requests to an identity provider.
    Define AUTH_OIDC_BUNDLE ../nicurl/ca-bundle.crt

    # Path to OIDC provider configuration.
    Define AUTH_OIDC_PROVIDER_DIR ${HTCONF_PATH}/openidc

    # The location to redirect when performing an OpenID-Connect login.
    Define AUTH_OIDC_REDIRECT_URI /login/openidc-redirect

    #
    # User-editable variables.
    #

    # Whether OIDC is enabled.
    Define AUTH_OIDC_ENABLED

    # When enabled, /login/openidc-redirect?info=json and
    # /login/openidc-redirect?info=html will return the claims for the currently
    # logged in user.
    Define AUTH_OIDC_ENABLE_CLAIM_INFO
    ```

If the provider is https with a certificate signed by a CA not included in the NI-CURL CA bundle (`C:\Program Files\National Instruments\Shared\nicurl\ca-bundle.crt`), then the `AUTH_OIDC_PROVIDER_DIR` define in `50_mod_auth_openidc-defines.conf` must to be updated to point to a CA bundle containing the provider's CA. The path can be absolute, or relative to `C:\Program Files\National Instruments\Shared\Web Server`.

### Mapping Claims to SystemLink Roles

Claims are returned as a JSON object.  

!!! note ""
    Example response from `userinfo_endpoint`. Use any of these claims to a map a user to a role in a workspace.
    ```json
    {
        "email": "jane.doe@ni.com",
        "family_name": "Doe",
        "given_name": "Jane",
        "name": "Jane Doe",
        "ni_employee": "2670",
        "sub": "jdoe"
    }
    ```

    Within the security UI the claim and its returned value can be mapped to a role within a Workspace.

    <figure>
      <img src="../../img/claim-mapping.png" width="500" />
      <figcaption>Mapping the ni_employee claim to a workspace.</figcaption>
    </figure>

If the claim value is a scalar, then it must exactly match the value specified in the role mapping. If the claim value is an array, then one of the array elements must exactly match the value specified in the role mappings.

If the claim value contains quotes the quotes must be escaped with \\.

!!! note "Example claim containing quotes"

    ```json
    {
      "userinfo": {
        "sub": "88442211",
        "country": "US",
        "name": "Bob Smith",
        "http://www.example.come/roles": [
          "user",
          "a\"b"
        ]
      }
    }
    ```

    <figure>
      <img src="../../img/escaped-claim.png" width="500" />
      <figcaption>Claims must be escaped with the \ character.</figcaption>
    </figure>

### Refreshing user claims

Claims are fetched at login. Log out and log back in for updated claims to affect role mappings.

## Troubleshooting Failed Authentication

The following sources can be used to troubleshoot a failed connection.

**OpenID Connect Provider logs:** Consult your OpenID Connect Provider's documentation on the location of their application log files.

**NI Web Server Logs:** These are found at `C:\ProgramData\National Instruments\Web Server\logs\error.log`.

!!! note
    SystemLink uses log rotation therefore the latest logs may be in one of the numbered `error.log` files.

**Returned Claims:** See [**Viewing Claims Returned by a Provider**](#viewing-claims-returned-by-a-provider).

### Cache Shm Entry Size Max

If an "Internal Server Error" is encountered when attempting to log in, this may be an issue with the defined `OIDCCacheShmEntrySizeMax`. You can verify this is the issue by searching the NI Web Server logs for the following entries:
```
    oidc_cache_shm_set: could not store value since value size is too large
    oidc_cache_set: could NOT store X bytes in shm cache backend for key Y
```
To resolve this issue
- Open the following file in a text editor run as Administrator `C:\Program Files\National Instruments\Shared\Web Server\conf\defines.d\50_mod_auth_openidc-defines.conf.defaults`
- Find the line `Define AUTH_OIDC_CACHE_ENTRY_SIZE 66065`
- Modify `66065` to a number larger than X, where X is the required size of the shm cache entry specified in the error log entry
    - It is suggested to follow the [documentation](https://github.com/zmartzone/mod_auth_openidc/blob/master/auth_openidc.conf#L600https://github.com/zmartzone/mod_auth_openidc/blob/master/auth_openidc.conf#L600) when changing this number
- Restart the NI Web Server from the `Control` tab of the NI Web Server Configuration application
