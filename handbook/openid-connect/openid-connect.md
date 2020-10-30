# Authenticating with OpenID Connect

You may configure SystemLink to use [OpenID Connect](https://openid.net) for user authorization. This enables SystemLink to leverage corporate single sign-on (SSO) and the additional security benefits it provides such as multi-factor authentication (MFA), streamlined login, and limiting the proliferation of user credentials between applications. This also enables SystemLink to utilize the common identity for users across multiple applications. 

## Assumptions and Prerequisites

- A server running SystemLink 2020R4 or greater. Please see [Installing and Configuring SystemLink Server and Clients](https://www.ni.com/documentation/en/systemlink/latest/setup/configuring-systemlink-server-clients/) for the basics of setting up a SystemLink server. 
- A DNS name for the SystemLink server. 
- SystemLink login with the **Server Administrator** role. 
- Administrator desktop access to the SystemLink server
- A OpenID Connect OpenID Provider (OP) server such as [PingFederate](https://www.pingidentity.com/en/software/pingfederate.html), [Azure ADFS](https://docs.microsoft.com/en-us/windows-server/identity/ad-fs/deployment/how-to-connect-fed-azure-adfs), [Okta](https://www.okta.com/openid-connect/), or another [certified OP](https://openid.net/certification/) that has been fully setup and configured for OpenID Connect authentication. 
    - If you have not yet setup your OP please consult the vendor documentation for setup and configuration. 

## Enabling OpenID Connect in SystemLink
1. Log into the server running SystemLink and open **NI Web Server Configuration**
2. Go to the **Authentication** tab and enable **OpenID Connect**

## Setting the OpenID Configuration in SystemLink server

There are three files that must be created to connect your SystemLink server to an OpenID Connect OP, [dns].conf, [dns].client, and [dns].provider. The [dns] portion of each filename must tbe the URL encoded fully qualified domain name. 

**[dns].conf** describes the scopes SystemLink will request access to, and the text and icon for the OP login button and icon. 
```json
{
 "scope": "openid email",
 "ni-attributes": {
   "displayName": "Log in with PingFederate",
   "iconUri": "/login/assets/pf.png"
 }
}
```
In this example the `openid` and `email` scopes are requested. Additional scopes may be requested, and all requested scopes must be made available by your OP. Consult your OPs documentation on exposing scopes to clients. Each scope will contain claims that can be used to map to roles within workspaces in SystemLink. See [**Mapping OpenID Connect Claims to SystemLink Workspaces and Roles**](#mapping-openid-connect-claims-to-systemlink-workspaces-and-roles) for details. 

The `ni-attributes` section determines the text and (optionally) an icon to be shown in the SystemLink login page. The `iconUri` is relative to htdocs directory (C:\Program Files\National Instruments\Shared\Web Server\htdocs)

TODO SCREENSHOT OF LOGIN PAGE WITH BUTTON.  

### ClientID and Secret in PingFederate
TODO describe where this information can be found, and link to PF documentation as much as possible. 

### Setting Login redirect URL
TODO describe the url for redirection and the inclusion of the full DNS name

## Troubleshooting Failed Authentication
TODO describe how OP logs are useful, and also describe the location of ni web server logs and the error types that can inform OIDC miss-configuration. 

## Mapping OpenID Connect Claims to SystemLink Workspaces and Roles
TODO Describe how claims are used in role mapping, where users can get info about claims coming from the OP. Describe the workflow for the actual mapping. Make sure to mention this can be used for Server Administrator mappings as well. Reference SPD where possible rather than repeat its content. 