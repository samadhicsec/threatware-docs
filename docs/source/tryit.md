# Try It!

The easiest way to quickly try out threatware is to complete the (simplified) setup and then try out the 4 brief (~5 mins each) tutorials.

## Setup
### 1. Copy tutorial threat model (3 min)

1. Make you own copy (menu option `File->Make a copy`, and tick the `Copy comments and suggestions` box) of the [tutorial threat model](https://docs.google.com/document/d/1Dnf-vzzEu1q0fZozBC-fi-hjefds9wWkRt6VXrrN2yo/view).
1. In the newly copied threat model click the `Share` button and under `General Access` select `Anyone with the link` and give them `Viewer` access (the default).  This is required so the container running threatware locally will be able to access it.

:::{admonition} Warning
:class: warning
If creating a copy of the tutorial threat model using an enterprise/business Google account, there may be restrictions preventing you from sharing it to `Anyone with the link`.  If this is the case you'll have to use a personal Google account for this tutorial
:::

3. Copy the Google document ID from **your copy of the tutorial threat model** from your browser URL bar.

   Example: for `https://docs.google.com/document/d/1Dnf-vzzEu1q0fZozBC-fi-hjefds9wWkRt6VXrrN2yo/edit` the document ID is `1Dnf-vzzEu1q0fZozBC-fi-hjefds9wWkRt6VXrrN2yo`

4. For each of the threatware action links (there are 5 i.e. convert, verify, manage.create, manage.indexdata and manage.submit) referenced in the TUTORIAL lines at the top of your copy of the tutorial threat model
    1. Click the link, and then click the “Edit link” button
    1. Replace the `docloc` URL parameter (**it should be the last one**) in each link URL with the document ID you copied (in step 3) for your copy of the tutorial threat model (it will be different to the example above!).  This makes it so threatware will read your copy of the tutorial threat model, rather than the public one.

### 2. Create local git repo (1 min)

This step requires you have access to a Linux/Mac/Windows WSL environment.

To see how threatware can persist a copy of threat models and track their versions and approval status, a git repo is needed.  In practice an online git repo (e.g. Github, Gitlab etc) would be used, but for the purpose of trying threatware, you can create a temporary local repo.

Assuming you have `git` [installed](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git), run the following commands in a shell:

```shell
# Create a local directory to store your threat models
mkdir /tmp/threatmodels
cd /tmp/threatmodels
# Initialise the git repo
git init --initial-branch approved && git commit --allow-empty --allow-empty-message -m ""
```

### 3. Run the container (5 min)

The directory `/tmp/threatmodels` must exist before we run the container.

If you haven't already, [install docker](https://docs.docker.com/engine/install/) (you may have issues using Docker Desktop) or [podman](https://podman.io/docs/installation) (recommended), and run:

```shell
# Depending on how docker is installed, you may need to run the below command with sudo
docker run -d --rm --name=threatware.local --publish 9000:8080 --mount type=bind,src=/tmp/threatmodels,dst=/home/threatuser/threatmodels docker.io/threatwaretryit/api_threatware:latest
```
or 

```shell
podman run -d --rm --replace --name=threatware.local --publish 9000:8080 --mount type=bind,src=/tmp/threatmodels,dst=/home/threatuser/threatmodels --userns=keep-id docker.io/threatwaretryit/api_threatware:latest
```

To test this is working correctly open <http://localhost:9000/version> in a browser, and you should get back a version number e.g. `0.9.4`.

## TUTORIAL 1 & 2 (15 mins)

:::{tip}
If using Chrome you may want to install a JSON viewer extension e.g. [JSON Viewer](https://chromewebstore.google.com/detail/json-viewer/gbmdgpbipfallnflgajpaliibnhdgobh).

Firefox will already neatly format JSON responses to be easier to read.
:::

Tasks:
1. Go through the comments in your copy of the tutorial threat model labelled **TUTORIAL 1**.  This will demonstrate the `convert` action of threatware. (5 mins)
1. Go through the comments in your copy of the tutorial threat model labelled **TUTORIAL 2**.  This will demonstrate the `verify` action of threatware. (10 mins)

In summary, threatware is able to convert a threat model in a document to a machine readable format, and also apply a set of (configurable) validations to ensure correctness and consistency of threat models.

Creating a threat model and being able to convert it to a machine readable format and to verify it is correct, is great for the process of actually creating a threat model, but creating a threat model is only part of the process required to operationalise threat modelling across your company.  threatware has two more actions that help with the management of threat models; `manage.create` and `manage.submit`.  The following tutorials are about how to use a gitops approach (i.e. using a git repo as your source of truth) to managing threat models.

## TUTORIAL 3 (5 mins)

When managing threat models it is incredible useful to have a constant identifer for a threat model.  Often the threat model name is used for this purpose, but generally speaking that might not remain constant and is harder to work with than a more compact ID.  threatware can be used to help create this identifier and keep a record of all the created identifiers in a git repo, alongside the name and status of the threat model.

Tasks:
1. In your copy of the tutorial threat model, click on the `manage.create` link at the top in the TUTORIAL 3 line.  This should return a message saying the ID `SAI.TMD.1` has been created.  
1. You can now update the `Threat Model ID` row in the "Details" table with this new ID value (confusingly there are 2 tables called "Details" in the threat model, one at the top and one under Components, for the purpose of these tutorials we are referring to the one at the top of the threat model).
1. threatware also let's you retrieve information about a threat model using its ID.  In your copy of the tutorial threat model, click on the link `manage.indexdata` at the top in the TUTORIAL 3 line.

    But this fails!  That is because making state changing `manage.*` requests to threatware (like when we clicked `manage.create`) does nothing but create a branch in the git repo, yet `manage.*` requests that read data only read from the `approved` branch.  So although we created a new ID (when we clicked `manage.create`), it's not 'official' until the `create` branch (where the created ID was written) is merged onto the `approved` branch.  Let's do that now:

    ```shell
    cd /tmp/threatmodels
    git merge create
    ```

1. Now let's try that `manage.indexdata` link again?  This time it should return details about the threat model with ID `SAI.TMD.1`.

    This means that the central Security team can manage threat models through controlling the merging of branches to a git repo they control.  Moreover since git is being used there is a full history of all the changes that were made (and by who).

1. If you want to see the actual file in the git repo that contains this data, you can do:

    ```shell
    cd /tmp/threatmodels
    cat threatmodels.yaml
    ```

In summary, to allow for the management of threat models across your business, threatware is able to assing a unique document identifier to each threat model and keep a registry of all threat models (in a git repo).

## TUTORIAL 4 (5 mins)

Storing basic information about the threat models that have been created is good, but what we really want is to manage approvals of threat models and also capture the contents of the threat model in the git repo.

Tasks:
1. In your copy of the tutorial threat model, click on the `manage.submit` link at the top in the TUTORIAL 4 line (this will fail if you didn't complete TUTORIAL 3 and update the ID in the "Details" table of the threat model).  The response should indicate that the threat model was submitted.  
1. We can confirm this by looking for a new branch in our git repo that matches the ID of the threat model (i.e. you should see a branch listed called `SAI.TMD.1`):

    ```shell
    cd /tmp/threatmodels
    git branch
    ```

Submitting threat models for approval via threatware is useful, but we also want threat models to be self-contained i.e. you should know the approval status of a threat model by just looking at the threat model itself.  

The approval status of the threat model is stored in the threat model itself using 2 tables:

- "Details" table 
    - the `Approved Version` row holds the last version of threat model that was approved (or it is empty if no version has been approved yet).
    - the `Current Version` row holds the version of the threat model being worked on.  This usually starts at `1.0` and increments from there.  It can be different to the `Approved Version` value, but should have a corresponding row in the "Version History" table.
- "Version History" table - contains a history of versions, with 1 row per version
    - `Version` holds the version identifier (there must be a row where the value in this column matches the versions listed in the "Details" table)
    - `Status` must be one of; `DRAFT`, `APPROVED`, or `OBSOLETE` (these values are configurable)
    - `Approver Name` must be populated if `Status` is `APPROVED`
    - `Approver Date` must be populated if `Status` is `APPROVED`

3. The action of approving the threat model it is expected to be done by someone with the appropriate authority, often someone from the Security team.  Go ahead and set the status of your copy of the tutorial threat model to approved by completing the below steps:
    - In the "Details" table set the `Approved Version`  to `1.0`
    - In the "Version History" table for the row with `Version` value `1.0`
        - Set the `Status` to `APPROVED` (I like to also change the table cell color to green)
        - Set an `Approver Name` (you can type `@` in the table cell to get Google to display a list of users)
        - Set an `Approver Date` (you can type `@date` in the table cell to bring up a calendar)

1. Now let's try clicking on the `manage.submit` link at the top in the TUTORIAL 4 line again.  You'll get a similiar message as last time, but it is really a reminder that the threat model isn't 'officially' approved until the branch threatware created in the git repo is merged onto the `approved` branch.  
1. Let's approve the threat model by merging onto the `approved` branch:

    ```shell
    cd /tmp/threatmodels
    git merge SAI.TMD.1
    ```

1. You can confirm that the current status of the threat model is approved by clicking on the `manage.indexdata` link from TUTORIAL 3 (the `status` field should say `APPROVED`).

In the git repo a new directory has appeared, named using the ID of the threat model you just approved.  Inside that directory are the following files:
- `metadata.yaml` - this contains metadata about each approved version of the threat model
- `1.0.plain.yml` - this contains the output of the `convert` command (the file name matches the version, so all old versions are kept and never overwritten)
- `1.0.yml` - this contains the same threat model data as `1.0.plain.yml` but includes internal metadata of threatware making it possible for threatware to read the threat model without having to reprocess the threat model.

In summary, you have used threatware (and git) to track the version, status and approvals for a threat model, and also captured the threat model in a git repo, in a machine readable format (yaml).

## Cleanup
That's it, you've finished the tutorials.  To clean up you can run:
- `docker container stop threatware.local` (or `podman container stop threatware.local`) to stop the threatware container
-  ```shell
   cd /tmp
   # to remove the local git repo
   rm -rf threatmodels 
   ```

:::{note}
CONGRATULATIONS!  You have just tried out threatware!  I hope you found it interesting and will consider using it to help you on your threat modelling journey.

To learn more about the threat modelling process you can read the [](./create/overview.md).

To install threatware as an AWS Lambda function so everyone in your company can access it, you can read [](./configure/installation.md)
:::