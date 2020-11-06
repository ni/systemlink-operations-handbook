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

Before making changes to markdown files in the handbook, set up a
[Python virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)
for using [MkDocs](https://www.mkdocs.org):

1. Download and [install Python](https://www.python.org/)
   (NI recommends 3.8 or later)
2. (Optional) Create a virtual environment named `.venv` in the current
   directory by running `python -m venv .venv`. Each time you open a new
   command window, activate the environment before running `mkdocs` commands:
    - Windows users: run `.venv\Scripts\activate`
    - Linux or Mac users: run `source .venv/Scripts/activate`
3. Upgrade pip by running `python -m pip install --upgrade pip`
4. Install dependencies by running `pip install -r requirements.txt`

For more information and installation options, see
[MkDocs - Installation](https://www.mkdocs.org/#installation).

## Previewing Changes to Markdown Files

Preview changes you make to handbook content before you submit them. In the
MkDocs environment you set up, run the following command to start a local
testing server:

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

To access the preview, open a browser and navigate to <http://127.0.0.1:8000/>.
For more information and configuration options, see
[MkDocs - Getting Started](https://www.mkdocs.org/#getting-started).

## Authoring Handbook Chapters
- Review **chapter-template.md** and use as a starting point and reference to the structure and style of the handbook. 
- To add a chapter you must update the `nav` section of the `mkdocs.yaml` in this respository to reference the new markdown document.

## Building a Local Copy of the Handbook

The handbook uses MkDocs to produce a static HTML website that any web server
can host. Build your own local copy of this handbook to access it without
internet connectivity. In the MkDocs environment you set up, run the following
command to build a local copy:

```bash
$ mkdocs build
INFO    -  Cleaning site directory
INFO    -  Building documentation to directory: site
INFO    -  Documentation built in 0.52 seconds
```

MkDocs builds the content into a `site` subdirectory, which you can copy into
any web server. For more information about building, see
[MkDocs - Building the site](https://www.mkdocs.org/#building-the-site).

## Upgrading Python Dependencies

The included [requirements.txt](requirements.txt) file lists specific versions
of each dependency and transitive dependency needed to build the handbook. To
install the latest versions, reference the
[requirements-latest.txt](requirements-latest.txt) file instead, by running
`pip install -r requirements-latest.txt`.

Upgrading versions may require changes to [stylesheets](handbook/stylesheets)
or [overrides](overrides) files. Specifically, see the [patches README](patches)
for information about upgrading the mkdocs-material dependency.

After installing new versions, generate an updated requirements.txt file by
running `pip freeze > requirements.txt`.

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
