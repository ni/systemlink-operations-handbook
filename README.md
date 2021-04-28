# SystemLink Operations Handbook

This repository contains documentation, examples, and example config files for
IT professionals to use when managing more advanced configurations of
[NI SystemLink Server](https://www.ni.com/systemlink). For information about
how to install and use a SystemLink server, see the
[latest product manual on ni.com](https://www.ni.com/r/systemlinkmanual).

## Accessing Documentation

The handbook is divided into chapters and published as HTML accessible at
<https://operations.systemlink.io/>.

The markdown and other supporting files used to generate the handbook are
accessible within the [handbook directory](handbook).

## Contributing to the Handbook

See the [contributing guidelines](CONTRIBUTING.md) for how to submit
contributions to the operations handbook.

## Developer Setup

### Getting Ready for Development

Before making changes to markdown files in the handbook, set up a
[Python virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)
for using [MkDocs](https://www.mkdocs.org):

1. Download and [install Python](https://www.python.org/)
   (NI recommends 3.8 or later)
2. (Optional) Create a virtual environment named `.venv` in the current
   directory by running `python -m venv .venv`. Each time you open a new
   command window, activate the environment before running `mkdocs` commands:
    - Windows users: run `.venv\Scripts\activate`
    - Linux or Mac users: run `source .venv/bin/activate`
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

### Building a Local Copy of the Handbook

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
