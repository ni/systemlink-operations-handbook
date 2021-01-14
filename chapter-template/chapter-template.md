# Chapter Template title

Write a brief description and overview of the goal to be achieved with the workflows and documentation described in the chapter. This template provides guidance for formatting chapters, but you can change the format depending on the topic.

- *What goals does this chapter help achieve?*
- *What questions does this chapter answer?*
- *Why should I care about the contents of this chapter?*

## Assumptions and Prerequisites

Describe the tools or applications you need to successfully execute the workflow.

- *What version of SystemLink is needed?*
- *What state or configuration must SystemLink be in?*
- *Are there any licensing requirements that must be met?*
- *Are there third party applications that must be in place?*
- *Are there tools that must be installed to complete the workflows*

## Section N

Break down the rest of the chapter into sections and subsections as needed. These should describe workflows plus any context that other users might find helpful.

- *-Does this workflow use any common command line operations?*
- *How do I get started with installing or setting up any required tools?*

### Example formatting CLI, configuration and code

Introduce a code snippet with one-line admonition as necessary. Keep in mind these do not render in Github style markdown, but will be rendered correctly in the built MkDocs site.

!!! note ""
    The following shows how to apply using the `systemlinkcli`.

```bash
systemlinkcli --apply
```

Below the code snippet, add details about the result, arguments, key/pairs, functions, etc. that the operation needs. This should leave the user with a complete understanding of what the code snippet does. Use fenced code blocks when introducing the code, and use appropriate markup language. Use in-line code block markup to reference most commands, parameters, arguments, or tuples. However, if the reference is multiple lines, use fenced code blocks

### Inline images

Screen shots are encouraged, as they can help clarify workflows and make content easier to read. However, screenshots may also become outdated as the product changes.

Using inline HTML is recommended by MkDocs to allow for proper captioning.

```md
<figure>
  <img src="../oidc-webserver.png" width="500" />
  <figcaption>Enable OpenID Connect in NI Web Server</figcaption>
</figure>
```



