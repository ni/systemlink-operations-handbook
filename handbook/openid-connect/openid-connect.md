# Authenticating with OpenID Connect

You may configure SystemLink to use [OpenID Connect](https://openid.net) for user authorization. This enables SystemLink to leverage corporate single sign-on (SSO) and the additional security benefits it provides such as multi-factor authentication (MFA), streamlined login, and limiting the proliferation of user credentials between applications. This also enables SystemLink to utilize the common identity for users across multiple applications. 

## Assumptions and Prerequisites

- A server running SystemLink 2020R4 or greater. Please see [Installing and Configuring SystemLink Server and Clients](https://www.ni.com/documentation/en/systemlink/latest/setup/configuring-systemlink-server-clients/) for the basics of setting up a SystemLink server. 
- A DNS name for the SystemLink server. 
- Administrator desktop access to the SystemLink server
- A OpenID Connect OpenID Provider (OP) server such as [PingFederate](https://www.pingidentity.com/en/software/pingfederate.html), [Azure ADFS](https://docs.microsoft.com/en-us/windows-server/identity/ad-fs/deployment/how-to-connect-fed-azure-adfs), [Okta], or another certified OP that has been fully setup and configured for OpenID Connect authentication. 
    - If you have not yet setup your OP please consult the vendor documentation for setup and configuration. 

## Enabling OpenID Connect in SystemLink
TODO describe enabling in NI Web Server configuration 

## Setting the ClientID and Secret
TODO describe where

### ClientID and Secret in PingFederate
TODO describe where this information can be found, and link to PF documentation as much as possible. 

## Troubleshooting Failed Authentication
TODO describe how OP logs are useful, and also describe the location of ni web server logs and the error types that can inform OIDC miss-configuration. 

## Mapping OpenID Connect Claims to SystemLink Workspaces and Roles
TODO Describe how claims are used in role mapping, where users can get info about claims coming from the OP. Describe the workflow for the actual mapping. Make sure to mention this can be used for Server Administrator mappings as well. Reference SPD where possible rather than repeat its content. 