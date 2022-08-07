# Management

The threatware `manage` actions (see [](../actions/manage.md)) cause threatware to store/retrieve threat model approval status, metadata, and model data in a storage location.

The only currently supported storage location is git.

## Setup

To enable this functionality an empty git repo needs to be created and the git remote URL populated in `manage/manage_config.yaml` configuration file under the `manage-config/storage/gitrepo/remote` key.

Either the user running threatware in a CLI environment, or the git credentials given the threatware running in AWS lambda, need permissions to create branches and push changes to this repo.

## Content

By default, threatware will create the following dir structure in the git repo (over time, as threatware `manage` actions are invoked on threat models) using a default branch called `approved` (this is configurable):

```
├── threatmodels.yaml
├── CMP.TM.1
    ├── metadata.yaml
    ├── 1.0.yaml
    ├── 1.0.plain.yaml
    ├── 1.1.yaml
    ├── 1.1.plain.yaml
├── CMP.TM.2
    ├── metadata.yaml
    ├── 1.0.yaml
    ├── 1.0.plain.yaml
├── CMP.TM.3
    ├── metadata.yaml
    ├── 1.0.yaml
    ├── 1.0.plain.yaml
└── ...
```

Where
- `threatmodels.yaml` is the source of truth for the approval status and approval metadata for all threat models.  The name of the file is configurable.
- Directories `CMP.TM.1` etc. contain the version history (in `metadata.yaml`) and approved models of each version of a threat model (`1.0.yaml` contains the 1.0 version of the threat model model-data with all metadata included, `1.0.plain.yaml` just contains the model-data and is meant to be more human readable).  The name of the directory is taken from the `IDprefix` parameter of the `manage.create` action, with a sequential number appended.

:::{admonition} Tip
threatware has not been tested with all git servers, so it may be necessary to manually create the default `approved` branch as a one time setup activity.
:::

## Purpose

When
- `manage.indexdata` is called it returns status metadata about a threat model from `threatmodels.yaml` file on the `approved` branch.
- `manage.create` is called it creates a `create` branch and appends to the contents of `threatmodels.yaml` a new threat model status metadata entry, and sets its status to `DRAFT`.  Multiple calls to `manage.create` append entries to the updated `threatmodels.yaml` in the `create` branch (so multiple calls to `manage.create` don't end up with the same threat model ID).
- `manage.submit` is called 
    - it creates a branch with the name of the threat model ID (e.g. `CMP.TM.1`), and 
    - updates the existing status metadata entry in `threatmodels.yaml` for a threat model to `APPROVED`, and 
    - adds or updates the directory named after the threat model ID (e.g. `CMP.TM.1`), 
        - adding/updating `metadata.yaml` with the version metadata of the submitted threat model, and 
        - adding the `1.0.yaml` and `1.0.plain.yaml` model files (with appropriate version number in the name e.g. if the submitted threat model had approved version 3.2 the files would be called `3.2.yaml` and `3.2.plain.yaml`).
- `manage.measure` is called is reads `threatmodels.yaml` from the `approved` branch to find the approved version of the submitted threat model, then loads the full metadata version of the threat model (e.g. `1.0.yaml`) from the repo, to use to compare against the current version of the threat model in the threat model document (passed in as a parameter to `manage.measure`).

## Process

As the storage location holds the source of truth for the approval status of a threat model, but anyone in an organisation can invoke `manage.create` and `manage.submit` (only these 2 actions change the state of the storage location), there needs to be a process to ensure that only approved changes are recorded.

This is the purpose of the `create` and threat model ID named (e.g. `CMP.TM.1`) git repo branches.  While anyone can cause entries on these branches to be created, only an approver should merge these changes onto the `approved` branch, thus making any changes official.

There therefore needs to be a set of official approvers with permission to merge changes onto the `approved` branch, usually the approvers would come from the Security Team in an origanisation.  The exact process for notifiying approvers about threat model updates is not specified, but when an threat model author uses threatware `manage.create` or `manage.submit` the git server can usually be configured to notify a group of people about the change, who can then carry out a process (via a defined runbook for example) to review the requested change and approve it if it is acceptable.