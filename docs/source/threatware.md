# threatware
Simplifies the review and management of threat models in documents

threatware is an AWS lambda function (or CLI tool) with methods to help review threat models and provide a process to manage threat models.  It works directly with threat models as Confluence/Google Docs documents.

## TL;DR
2 things:
- When capturing a threat model in a document, threatware can help answer the question ['Did we do a good job?'](https://github.com/adamshostack/4QuestionFrame), because it can verify the referential integrity of the information in the document (i.e. nothing undefined is referenced) and that there are threats covering all the assets.  This gives some assurance that your threat model is complete.  In contrast, many threat modelling tools take input and generate threats, but are unable to provide any assurance.
- threatware provides a management framework to track, approve and iterate a threat model document.  There is no lock-in, all information is stored in a git repo.  The information it captures could be used for a variety of data-driven purposes e.g. inventory, coverage, metrics, etc.

# Installation

threatware requires a recent version of `python` (3.9 or above, and you should have `pip` installed as well ([instructions](https://pip.pypa.io/en/stable/installation/))) and that a recent version of `git` is installed ([instructions](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)).  You may also want to consider installing threatware in a [virtual environment](https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-and-using-virtual-environments)

`python3 -m pip install threatware`

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
- threatware documentation includes detailed instructions on how to populate the template, aimed at developers, not threat modelling experts. (scalable)
- threatware can verify the populated Threat Model template and report back on errors and missing threats. (automation) 
- threatware can help define a management process for threat models by storing versioned: status, metadata and a model of your Threat Model document in a git repo of your choice. (auditors love this)

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
3. Identify the people who need to populate the template (i.e. system owners/experts) and point them at the documentation and how to invoke threatware `verify`
4. Have sessions to begin populating the threat model.  Use threatware `verify` to make sure no information is missing (look for `reference-validation` errors first).  You'll like need 3-5 sessions, including off-line time spent populating.
5. Use threatware `verify` to make sure your have threats covering all your assets (look for `coverage-validation` errors)
6. Once threatware `verify` returns no errors, sense check the threat model for completness
7. Get someone appropriate in your organisation to add their approval to the threat model
8. Use threatware `submit` to create a record of the approved threat model in a git repository

See [](./create/overview.md#the-threat-modelling-process) for a more in-depth explanation of the process.

As 3-4 threat models are completed, your local threat model template can be updated to include common components, assets and threats, which makes the next threat models easier to complete.  It's fine to add things that might not be relevant to some systems, as removing them from the copy of your threat model template is easy.

### AWS lambda

See [](./configure/authentication.md) for full details on how to configure authentication.

Put Confluence/Google credentials, and git credentials into [AWS Secret Store](./configure/authentication.md#authentication-for-threatware-aws-lambda).  Change `manage/manage_config.yaml` to point to your chosen git repo.

Setup [dynamic configuration](./configure/configuration.md#dynamic-configuration) to have your custom configuration in your own git repo.

Clone the [repo](https://github.com/samadhicsec/threatware) and build the dockerfile. Upload docker image to ACS.  Create AWS lambda using docker image.  Adjust timeout on lambda to 30 seconds (you may need to increase memory if you get timeouts).  

Trigger lambda via API Gateway (please restict access to your lambda to at least your organisation's IP range).

### CLI

See [](./configure/authentication.md) for full details on how to configure authentication.

Run `threatware convert -s abc -d 123`, this will fail, but the configuration will be downloaded (from this [repo](https://github.com/samadhicsec/threatware-config)).

Put Confluence credentials in `~/.threatware/.atlassian`.  Google Doc credentials will be automatically capture on first attempt to access a Google Doc (requires creating [Google App credentials](./configure/authentication.md#google-docs) first). threatware will use your existing git credentials SSH keys.  Change `manage/manage_config.yaml` to point to your chosen git repo.

Run `threatware -h` to see command line options.