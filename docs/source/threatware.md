# threatware
Simplifies the review and management of threat models in documents

threatware is an AWS lambda function (or CLI tool) with methods to help review threat models and provide a process to manage threat models.  It works directly with threat models as documents in Confluence/Google Docs.

## TL;DR for developers
- threatware is a compiler for threat models.  For threat models as documents (in a format you can define), threatware reads and validates the document and can output the threat model in a machine-readable language.
- threatware is a change management system for threat models.  threatware can be used as part of a GitOps process for approving threat models (whether new or as updates to existng threat models).

## TL;DR for security teams
- threatware helps your threat modelling to scale.  Engineering teams authoring their own threat models as documents (in a format you can define), can use threatware to detect errors in the threat model, as it is populated.  threatware documentation contains the process, guidance and examples to empower engineering teams to be threat model authors (with help from a security team).
- threatware helps you govern your threat modelling.  threatware provides a management framework to track and approve new threat models and updates to existing threat models.

# Installation

## CLI

threatware requires a recent version of `python` (3.9 or above, and you should have `pip` installed as well ([instructions](https://pip.pypa.io/en/stable/installation/))) and that a recent version of `git` is installed ([instructions](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)).  You may also want to consider installing threatware in a [virtual environment](https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-and-using-virtual-environments)

`python3 -m pip install threatware`

Run `threatware convert -s abc -d 123`, this will fail, but the default configuration will be downloaded (from this [repo](https://github.com/samadhicsec/threatware-config)).

Run `threatware -h` to see command line options.

## AWS Lambda

threatware on AWS Lambda requires uploading a docker image for the lambda function to execute, setting authentication credentials in AWS Secrets Manager, and configuring API Gateway to invoke the lambda (as well as a bunch of IAM configuration).  Full instructions on the installation can be found in [](./configure/installation.md#aws-lambda).

## Configuration

See [](./configure/configuration.md) for details on how to setup the configuration location and files required by threatware

See [](./configure/authentication.md) for details on how to configure authentication for threatware so it can access Confluence, Google Docs, and git.

See [](./configure/management.md) for details on how to setup a storage location to store threat model management data.

# Download

threatware is available on PyPI <https://pypi.org/project/threatware/>

The documentation is hosted at: <https://threatware.readthedocs.io>

# Code

The code and issue tracker are hosted on GitHub: <https://github.com/samadhicsec/threatware>

# Details

## Who is this for?

It's for people/teams who do threat modelling or want to do threat modelling.

threatware has different features to suit those who are beginning to threat model, and those who are experienced.

### Beginners

- threatware provides a [Threat Modelling template](./create/template.md) that works out of the box.  The template is available as either a Confluence page or a Google Doc. (no tool lock-in)
- threatware [documentation](./create/overview.md) includes detailed instructions on how to populate the template, aimed at developers, not threat modelling experts. (scalable)
- threatware can [verify](./actions/verify.md) the populated Threat Model template and report back on errors and missing threats. (automation) 
- threatware can help define a [management](./configure/management.md) process for threat models by storing versioned: status, metadata and a model of your Threat Model document in a git repo of your choice. (auditors love this)

### Intermediates

- minor changes to the template (new table columns, changing header names) can easily be supported to allow capturing relevant data for your organisation. (flexible)
- the basic Threat Modelling template can be pre-populated with common information relevant to different systems. (less effort to populate)
- create many different templates for different tech stacks, with appropriate pre-populated values. (more relevant, less effort to populate)
- threatware supports localisation. (increase adoption)

### Experts

- threatware allows extensive customisation of the template, by defining your own 'scheme' (which is used to parse the threat modelling document - it's a custom document definition language, sorry, we couldn't find an existing one that worked).  If you have existing documents or specific information that you want gathered, you can define this.
- the template can be part of existing product/system documentation, threatware will extract the relevant information (as defined by the 'scheme')
- the verification of the threat model is customisable, and defined in configuration files, which allows enabling/disabling verification rules, or adding additional rules
- the verification of the threat model is extensible (in python), as verification methods are dispatched via configuration files, so you can easily extend threatware by writing your own verifiers and updating configuration files to get them called

## How do I use it?

Of course that is up to you, but here is an idea of how it has been successfully used (assuming you have installed threatware and configured it):

1. Make a copy of the threat model template available somewhere in your orgnisation i.e. copy the default template somewhere local to your organisation
2. When you need to create a threat model, make a copy of your local threat model template.  This will be the document you edit.
3. Identify the people who need to populate the template (i.e. system owners/experts) and point them at the [documentation](./create/overview.md) and how to invoke threatware `verify`
4. Have sessions to begin populating the threat model.  Use threatware `verify` to make sure no information is missing (look for `reference-validation` errors first).  You'll like need 3-5 sessions, including off-line time spent populating.
5. Use threatware `verify` to make sure your have threats covering all your assets (look for `coverage-validation` errors)
6. Once threatware `verify` returns no errors, sense check the threat model for completness
7. Get someone appropriate in your organisation to add their approval to the threat model
8. Use threatware `submit` to create a record of the approved threat model in a git repository

See [](./create/overview.md#the-threat-modelling-process) for a more in-depth explanation of the process.

As 3-4 threat models are completed, your local threat model template can be updated to include common components, assets and threats, which makes the next threat models easier to complete.  It's fine to add things that might not be relevant to some systems, as removing them from the copy of your threat model template is easy.
