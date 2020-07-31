# Contributing to SystemLink Operations Handbook

Contributions to SystemLink Operations Handbook are welcome from all!

systemlink-operations-handbook is managed via [git](https://git-scm.com), with
the canonical upstream repository hosted on
[GitHub](https://github.com/ni/systemlink-operations-handbook).

systemlink-operations-handbook follows a pull-request model for development. If
you wish to contribute, you will need to create a GitHub account, fork this
project, push a branch with your changes to your project, and then submit a
pull request.

See [GitHub's official documentation](https://help.github.com/articles/using-pull-requests/)
for more details.

## Developer Setup

Before making changes to markdown files in the handbook, developers should set
up a [MkDocs development environment](https://www.mkdocs.org/#installation).
The most consistent way is manually, through Python:

1. Download and [install Python](https://www.python.org/)
   (3.8 or later is recommended)
2. (Optional) Create a virtual environment named `mkdocs` in the current
   directory: `python -m venv mkdocs`
3. (Optional) Activate the virtual environment by running `activate` in the
   `Scripts` sub-directory of the `mkdocs` virtual environment
4. Upgrade pip: `python -m pip install --upgrade pip`
5. Install dependencies: `pip install -r requirements.txt`

## Previewing Changes to Markdown Files

When making a change to handbook content, use the
[MkDocs environment](https://www.mkdocs.org/#getting-started) set up in the
Developer Setup section to start a local testing server:

```bash
$ mkdocs serve
INFO    -  Building documentation...
INFO    -  Cleaning site directory
INFO    -  Documentation built in 0.58 seconds
[I 200731 15:48:28 server:334] Serving on http://127.0.0.1:8000
INFO    -  Serving on http://127.0.0.1:8000
[I 200731 15:48:28 handlers:62] Start watching changes
INFO    -  Start watching changes
[I 200731 15:48:28 handlers:64] Start detecting changes
INFO    -  Start detecting changes
```

Then open a browser to <http://127.0.0.1:8000/> to access a preview of the your
local copy of the handbook.

## Building a Local Copy of the Handbook

The handbook uses MkDocs to produce a static HTML website that can be served by
any web server. To make the handbook available offline, you can build your own
copy of the handbook using the
[MkDocs environment](https://www.mkdocs.org/#building-the-site) set up in the
Developer Setup section:

```bash
$ mkdocs build
INFO    -  Cleaning site directory
INFO    -  Building documentation to directory: site
INFO    -  Documentation built in 0.52 seconds
```

The content is built into a `site` subdirectory, which can be copied into any
web server.

## Developer Certificate of Origin (DCO)

   Developer's Certificate of Origin 1.1

   By making a contribution to this project, I certify that:

   (a) The contribution was created in whole or in part by me and I
       have the right to submit it under the open source license
       indicated in the file; or

   (b) The contribution is based upon previous work that, to the best
       of my knowledge, is covered under an appropriate open source
       license and I have the right under that license to submit that
       work with modifications, whether created in whole or in part
       by me, under the same open source license (unless I am
       permitted to submit under a different license), as indicated
       in the file; or

   (c) The contribution was provided directly to me by some other
       person who certified (a), (b) or (c) and I have not modified
       it.

   (d) I understand and agree that this project and the contribution
       are public and that a record of the contribution (including all
       personal information I submit with it, including my sign-off) is
       maintained indefinitely and may be redistributed consistent with
       this project or the open source license(s) involved.

(taken from [developercertificate.org](https://developercertificate.org/))

See [LICENSE](https://github.com/ni/systemlink-operations-handbook/blob/master/LICENSE)
for details about how systemlink-operations-handbook is licensed.
