# Chapter Template title

Within the title section should be a brief description and overview of the goal to be achieved with the workflows and documentation described in the chapter. Please note, this template is to provide guidance on the format for chapters, but this format can and should be changed depending on the topic. 

- *What goals will be achieved?*
- *What questions will be answered?*
- *Why should I care about the contents of this chapter?*


## Assumptions and Prerequisites

This section should describe the tools or application that must be in place in order for the workflow to be successfully executed. 

- *What version of SystemLink is needed?*
- *What state or configuration must SystemLink be in?*
- *Are there any licensing requirements that must be met?*
- *Are there third party applications that must be in place?*
- *Are there tools that must be installed to complete the workflows*

## Section N

The remainder of the chapter should be broken down in the sections and subsections as needed. These should describe the workflow to be completed as well as the theory or underlying details that provide context to why the workflow is setup as it. 

- *Are there common command line operations that should be used/understood?*
- *How do I get started with installing or setting up any required tools?*

### Example formatting CLI, configuration and code. 

Begin with a single sentence introducing the snippet and what is accomplishes.

```bash
systemlinkcli --apply
```

Below the snippet should be additional details regarding the result of the operations and the arguments, key/pairs, functions, etc that can/must be included to complete the operation. This should be several sentences long and leave the user with a complete understanding. Fenced code blocks should always be used when introducing the command/configuration/code, and the code block should be marked up with the language such that appropriate formatting may be applied. In-line code block markup should be used when referencing any particular command/parameter/argument/tuple unless that reference is multiple lines. In that case fenced code blocks should again be used. 
