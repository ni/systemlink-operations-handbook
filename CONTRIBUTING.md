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

## When to add content to the handbook

Add content to the SystemLink Operations Handbook in any of the following situations:

- The primary audience for this content is IT professionals.
- The content is primarily example code.
- The content covers more advanced or corner-case scenarios than the [ni.com help](https://www.ni.com/documentation/en/systemlink/latest/manual/manual-overview/).
- Customers need the content sooner than the current release timeline can deliver it.
- The content covers a preview feature. If this is the case, remember to add a note saying so.

Otherwise, raise an issue in GitHub or leave feedback on ni.com to request help content.

## Authoring Handbook Chapters

- Review **chapter-template.md** and use as a starting point and reference to the structure and style of the handbook.
- To add a chapter, update the `nav` section in `handbook/.pages` in this repository to reference the new chapter directory.

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

## Linting Markdown Files

All markdown must pass linting rules before a PR may be merged. The [markdownlint plugin for VSCode](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint) is recommended. The `.markdownlint.yaml` file contains overrides to linting rules for the handbook.

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
