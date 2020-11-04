# Authenticating with OpenID Connect

You may configure SystemLink to use [OpenID Connect](https://openid.net) for user authorization. This enables SystemLink to leverage corporate single sign-on (SSO) and the additional security benefits it provides such as multi-factor authentication (MFA), streamlined login, and limiting the proliferation of user credentials. This also enables SystemLink to utilize the common identity for users across multiple applications. OpenID connect can be used in conjunction with or as a replacement for LDAP, ActiveDirectory, and local Windows accounts for authentication. 

## Assumptions and Prerequisites

- A server running SystemLink 2020R4 or greater. Please see [Installing and Configuring SystemLink Server and Clients](https://www.ni.com/documentation/en/systemlink/latest/setup/configuring-systemlink-server-clients/) for the basics of setting up a SystemLink server. 
- A DNS name for the SystemLink server. 
- SystemLink login with the **Server Administrator** role. 
- Administrator desktop access to the SystemLink server
- A OpenID Connect OpenID Provider server such as [PingFederate](https://www.pingidentity.com/en/software/pingfederate.html), [Azure ADFS](https://docs.microsoft.com/en-us/windows-server/identity/ad-fs/deployment/how-to-connect-fed-azure-adfs), [Okta](https://www.okta.com/openid-connect/), or another [certified provider](https://openid.net/certification/) that has been fully setup and configured for OpenID Connect authentication. 
    - If you have not yet setup your provider please consult the vendor documentation for setup and configuration. 

## Enabling OpenID Connect in SystemLink
1. Log into the server running SystemLink and open **NI Web Server Configuration**
2. Go to the **Authentication** tab and enable **Use OpenID Connect (advanced)**

![Enable OpenID Connect in NI Web Server](odic-webserver.png)
*Enable OpenID Connect in NI Web Server*

## OpenID Configuration Files in SystemLink server

There are three files that must be created to connect your SystemLink server to an OpenID Connect provider, `[provider-dns].conf`, `[provider-dns].client`, and `[provider-dns].provider`. The `[provider-dns]` portion of each filename must tbe the URL encoded fully qualified domain name. 

These files do no exist for new SystemLink installations. Each of these file must be created in the `C:\Program Files\National Instruments\Shared\Web Server\conf\openidc` directory. The NI Web Server must be restarted for these changes to take effect. 

SystemLink can be configured to support multiple OpenID Providers simultaneously. It is required that the user ID used in SystemLink be unique across providers. This id take the form `[sub_claim]@issuer` where this issuer is the DNS name of the OpenID Connect provider. You can see the id SystemLink uses for a user by viewing the details of that user in the SystemLink security application.  

### SystemLink Login Window Configuration

**[provider-dns].conf** describes the scopes SystemLink will request access to, and the text and icon for the provider login button and icon. 
```json
{
 "scope": "openid email profile",
 "ni-attributes": {
   "displayName": "Log in with PingFederate",
   "iconUri": "/login/assets/pf.png"
 }
}
```
In this example the `openid`, `email`, and `profile` scopes are requested. Additional scopes may be requested, and all requested scopes must be made available by your provider. Consult your OPs documentation on exposing scopes to clients. Each scope will contain claims that can be used to map to roles within workspaces in SystemLink. See [**Mapping OpenID Connect Claims to SystemLink Workspaces and Roles**](#mapping-openid-connect-claims-to-systemlink-workspaces-and-roles) for details. 

The `ni-attributes` section determines the text and (optionally) an icon to be shown in the SystemLink login page. The `iconUri` is relative to htdocs directory (`C:\Program Files\National Instruments\Shared\Web Server\htdocs`)

After setting this configuration the NI Web Server must be restarted for changes to take effect. 

![SystemLink login windows with SSO login option](login-window.png)
*SystemLink login windows with SSO login option. An icon has not been set in this example.*

### ClientID and Secret 
The [provider-dns].client file is used by the NI Web Server to authenticate with the provider. 

```json
{
 "client_id": "slserver",
 "client_secret": "4vFm89u07xaredactedredactedredactede2tjtsEGQhlLreLVjcyLA0"
}

```
The `client_id` and `client_secret` can be obtained directly from the provider. Depending on the provider the `client_id` may be user defined. After setting these properties the NI Web Server must be restarted for changes to take effect. 

#### Provider Documentation

[PingFederate - Configuring an OAuth Client](https://docs.pingidentity.com/bundle/pingfederate-93/page/roj1564002966901.html)

[Using OAuth 2.0 to Access Google APIs](https://developers.google.com/identity/protocols/oauth2)

[Okta - Find your Application's credentials](https://developer.okta.com/docs/guides/find-your-app-credentials/findcreds/)

### OpenID Configuration and Discovery
The contents of the OpenID provider configuration must be copied in the [provider-dns].provider file. This file informs SystemLink of of the various endpoints exposed by the provider that are used during the login process. 

```bash
curl https://[provider-dns]/.well-known/openid-configuration -o [provider-dns].provider
```

### Setting Login Redirect URI
The client configuration for your provider requires a redirect URL that is during the login flow. This must include the protocol (`https://` or `http:// `) and the DNS name of the SystemLink server. If the SystemLink server's DNS changes, this setting must be updated with the provider. 

```url
[protocol]://[systemlink-dns]/login/openidc-redirect

```

## Mapping OpenID Connect Claims to SystemLink Workspaces and Roles

Once SystemLink and the provider have been configured such that users can authenticate and login, mappings between OpenID claims and workspaces must be made in order to provide the user access to systems and data managed by SystemLink. This process is the same as the mapping workflow for LDAP and Active Directory attributes, groups, and users. Please see [Assigning Users to Roles in a Workspace](https://www.ni.com/documentation/en/systemlink/latest/setup/mapping-roles/) in the SystemLink manual. Claims may also be used to create a mapping to the **Server Adminstrator** role. 

The OpenID Connect provider which scopes and claims are made available to clients. The available claims can be viewed at `userinfo_endpoint` hosted by the provider. Use `https://[provider-dns]/.well-known/openid-configuration` to determine the URL of `userinfo_endpoint`. You will need to obtain a valid Bearer token to be included in the request to this endpoint to return data. 

```bash
curl -s https://slsso-runtime.grl-us1.uat.k8s.com/idp/userinfo.openid -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiI...zJVy2oLnrBmXTmpDRm499U4~'|python -m json.tool
```
Example curl request to return user info. The bearer token has been shortened for readability. 

```json
{
    "email": "mark.black@ni.com",
    "family_name": "Black",
    "given_name": "Mark",
    "name": "Black",
    "ni_employee": "2670",
    "sub": "mblack"
}
```

Example response from `userinfo_endpoint`. Any of these claims may be used to map a user to a role in a workspace. 

![Mapping the ni_employee claim to a workspace](claim-mapping.png)
*Mapping the `ni_employee` claim to a workspace*

If a claim returns an array of values any one of these values can be supplied in the **Value** field to create a mapping. 

## Troubleshooting Failed Authentication
Due to the amount of configuration required by both the provider and SystemLink its can be challenging to enable the entire OpenID Connect flow. The following sources can be used to troubleshoot a failed connection. 

**OpenID Connect Provider logs:** Consult your OpenID Connect Provider's documentation on the location of their application log files. 

**NI Web Server Logs:** These are found at `C:\ProgramData\National Instruments\Web Server\logs\error.log`
