# Workspace and Role Based Access Control

In SystemLink 2020R2 NI introduced a new role based access control (RBAC) system. This security technology provides strong isolation between different *workspaces* as well as fine grain privileges for systems, data, and analysis routines in SystemLink. Collectively this capability allows access to SystemLink to scale beyond a single team to an entire organization.

## Concepts and design

SystemLink RBAC leverages concepts common to RBAC systems such as *roles* and *users*. It also introduces concepts such as *workspaces* and constraints such as *automatic data encapsulation* to better serve the needs of organizations performing device validation and production test.

### Workspace

A workspace is a complete encapsulation of all systems, data, and other resources within SystemLink. If a user is not a member of a given workspace they cannot access or modify any of the resources within the workspace. This is true for both from the SystemLink web application and through the SystemLink REST API. The SystemLink Advanced Server license is required to create multiple workspaces, but there is no limit on the number of workspaces that can be created. If a user is a member of multiple workspaces resource from each workspace will be shown together within the grids, dashboards, and other data views throughout SystemLink.

### Role

Within each workspace user and automated agents are assigned roles. Role grant privileges that allow access to the various SystemLink plugins and the data exposed by those plugins. Privileges explicitely grant what you *can* do - there are no *deny* privileges. Due to this a user may be assigned multiple roles within a single workspace that collectively describe what the user has access to. This is useful to prevent the proliferation of multiple different roles that have similar privileges. Instead simple roles may be defined and be composed together by assigning a user each role.

## Built in and custom roles

TODO make the point that users should have as little access as necessary to do there jobs. 

### Users

User's are backed by an identity provider (LDAP, Active Directory, OpenID Connect) that provides authenticated access to SystemLink. This is in contrast to systems and analysis routines that are managed within SystemLink and are not backed by an identity provider. Users may be members of multiple workspaces, but may have different roles in each workspace. This is useful when you want to leverage patterns such as all users having read-only access to multiple workspaces, but a few users have additional privileges in specific workspaces allowing a greater degree of access.

If a user is  a member of multiple workspaces, the resources in those workspaces will be shown simultaneously with the grids or other views within SystemLink. This is useful when users need to view a rollup of resources across multiple workspaces. All grids within SystemLink feature a workspace column and filters that can be used to limit the resources shown in a grid to a particular set of workspaces. While resources in multiple workspaces may be viewed in a single grid the actions a user can take against those resources may be different depending on their role in each workspace.

When a JupterNotebook is run either through the *Reports* feature of by a dashboard run with the same level of privileges as the user initiating the Notebook run. This is useful as it allows the creation of Notebooks that access data generally and do not need to have additional workspace logic. For example the built-in dashboard for Systems Management includes a tile that show the number of alarms for various systems. 

### Automated Agents

Automated Agents is a catch all term that applies to systems managed by SystemLink and analysis scripts executed by **Analysis Server**. 

### Automatic Data Encapsulation



## Mapping users to roles in workspaces

## Patterns for workspaces
