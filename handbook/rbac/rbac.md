# Workspace and Role Based Access Control

In SystemLink 2020R2 NI introduced a new role based access control (RBAC) system. This security technology provides strong isolation between different *workspaces* as well as fine grain privileges for systems, data, and analysis routines in SystemLink. Collectively this capability allows access to SystemLink to scale beyond a single team to an entire organization.

## Concepts and design

SystemLink RBAC leverages concepts common to RBAC systems such as *roles* and *users*. It also introduces concepts such as *workspaces* and constraints such as *automatic data encapsulation* to better serve the needs of organizations performing device validation and production test.

### Workspace

A workspace is a complete encapsulation of all systems, data, and other resources within SystemLink. If a user is not a member of a given workspace they cannot access or modify any of the resources within the workspace. This is true for both from the SystemLink web application and through the SystemLink REST API. The SystemLink Advanced Server license is required to create multiple workspaces, but there is no limit on the number of workspaces that can be created. If a user is a member of multiple workspaces resource from each workspace will be shown together within the grids, dashboards, and other data views throughout SystemLink.

### User and Role

Within each workspace user and automated agents are assigned roles. Role grant privileges that allow access to the various SystemLink plugins and the data exposed by those plugins. Privileges explicitly grant what you *can* do - there are no *deny* privileges. Due to this a user may be assigned multiple roles within a single workspace that collectively describe what the user has access to. This is useful to prevent the proliferation of multiple different roles that have similar privileges. Instead simple roles may be defined and be composed together by assigning a user each role.

#### Built in and custom roles

TODO make the point that users should have as little access as necessary to do there jobs.

#### Users

User's are backed by an identity provider (LDAP, Active Directory, OpenID Connect) that provides authenticated access to SystemLink. This is in contrast to systems and analysis routines that are managed within SystemLink and are not backed by an identity provider. Users may be members of multiple workspaces, but may have different roles in each workspace. This is useful when you want to leverage patterns such as all users having read-only access to multiple workspaces, but a few users have additional privileges in specific workspaces allowing a greater degree of access.

If a user is  a member of multiple workspaces, the resources in those workspaces will be shown simultaneously with the grids or other views within SystemLink. This is useful when users need to view a rollup of resources across multiple workspaces. All grids within SystemLink feature a workspace column and filters that can be used to limit the resources shown in a grid to a particular set of workspaces. While resources in multiple workspaces may be viewed in a single grid the actions a user can take against those resources may be different depending on their role in each workspace.

When a JupyterNotebook is run either through the *Reports* feature of by a dashboard run with the same level of privileges as the user initiating the Notebook run. This is useful as it allows the creation of Notebooks that access data generally and do not need to have additional workspace logic. For example the built-in dashboard for Systems Management includes a tile that show the number of alarms for various systems. This tile will only show systems within workspaces for which the current logged in user is member 

#### Service roles

Service roles are roles that that apply to systems managed by SystemLink and analysis scripts executed by **Analysis Automation**. Systems are always automatically assigned the built-in **Automated Agent** role. Analysis Automation routines can be configured to run with the built-in **Automated Agent** role, a user defined service role, with the privileges of the user initiating the analysis task, or with the TDM user, which is a role assigned to a Windows user on the SystemLink app server.

Any user defined role may be configured to be an automated agent role by toggling the **Service Role** checkbox in the role configuration modal slide out when the role is created. This cannot be changed after role creation. There are no restrictions on the privileges that may be applied to the role. It exists to signal to various SystemLink UIs what roles can be assigned to user and what roles can be assigned the systems and analysis routines. This forces the user to curtail roles appropriately to each scenario and avoid the proliferation of roles that grant greater access than is necessary to a user, system, or analysis routine.

TODO link to the TDM docs on the TDM user stuff
TODO screenshot of enabling automated agent role. 

### Automatic Data Encapsulation

When a system is added to SystemLink the user must choose which workspace the system will reside. The workspaces available to the user is determine by both their workspace membership and **Add systems** privilege. Once added to a workspace, data produced by the system will automatically be stored in the same workspace as the system. This capability allows users to author workspace agnostic test applications. Changing workspaces should not require the user to make changes or redeploy their test application. This is especially helpful when in scenarios such as production verification where the test application cannot change between validation and production but the data produced should only be accessible to specific individuals.

## Mapping users to roles in workspaces

Users must have a role within a workspace. To facilitate this mappings are defined within the context of workspace of the role they are assigned. This allows for users to be assigned different roles in different workspaces if desired.

Users are added to a workspace and assigned a role through a process called *workspace and role mapping*. The process is driven by meta data provided by the identity provider (IdP) user to authenticate users for SystemLink: OpenID Connect, LDAP, Active Directory, and local Windows accounts. Refer to the documentation for each of these IdPs for details on how to configure SystemLink for workspace and role mapping. By using meta data from an IdP you can create mappings that on-board large numbers of users into SystemLink. It also allows users to leverage existing Active Directory and LDAP groups.

## Patterns for workspaces

**Strict Isolation**

**Production and Production verification**

**Matrixed Support Roles**

**Management Roll-up**