# manage

The `manage` action is actually 4 different actions, all related to managing the threat modelling process.

The `manage` actions allow:
- A threat model author to `create` a threat model ID for their new threat model
- A threat model author or approver to `submit` a threat model for approval
- A threat model author to `check` whether changes to an existing threat model require approval
- Querying the `indexdata` (i.e. metadata) relating to whether a threat model is approved or not

## manage.create

The purpose of `manage.create` is to enable a threat model author to ask for a new threat model ID to be created.  The new ID is returned as a result of this request, but the new ID is not official until it is approved in the storage management data storage location i.e. by default the storage location is a git repo, and the new ID needs to be merged from the `create` to the `approved` branch.  If multiple `manage.create` requests are made before an outstanding new ID is approved, the new requests are added to the existing request to be approved (note, this works different to other requests like `manage.submit`).

`manage.create` takes the following parameters
- `IDprefix` - this can be any string.  A recommended format is a 3-letter company abbreviation, followed by `TMD` (Threat Model Document), e.g. `CMP.TMD`.  This prefix forms part of the new threat model ID, with a unqiue number added to the suffix, making a the final threat model ID, for instance `CMP.TMD.4`.  There is freedom here to choose a naming convention that suits, and you may find it appealing to mirror your company hierarchy.  Whatever the prefix is that is chosen, the goal of `manage.create` is to assign a unique number to each threat model, and for the resulting threat model ID to be a short and succinct identifier for the threat model.
- `scheme` - the scheme name of the scheme required to parse the new threat model.  `manage.create` will verify that the `docloc` is not already associated a another threat model ID.
- `docloc` - the document ID of the new threat model document.  `manage.create` will verify that the `docloc` is not already associated a another threat model ID.

Examples:

Using `manage.create` with threatware as a lambda, to create a new threat model ID for a threat model document in Confluence:

    https://<lambda-url>/threatware?action=manage.create&IDprefix=CMP.TMD&scheme=confluence_1.0&docloc=123456

Using `manage.create` threatware as a CLI, to create a new threat model ID for a threat model document in Google Docs:

    python3 -m actions.handler manage create -IDprefix CMP.TMD -scheme googledoc_1.0 -docloc 123456

Note, when using the CLI we pass in `create` as a sub-command to `manage` i.e. `manage create` (note the space separating them, not a `.`).

## manage.submit

The purpose of `manage.submit` is to submit a threat model for approval.  There are 2 use cases:
- The threat model author wants to inform a threat model approver that the threat model is ready for review to be approved.  The threat model author invokes `manage.submit` and this creates a submitted threat model in the management data storage location, which an approver can detect, and then schedule the threat model for review (the exact process via which an approver detects a submit is out of scope for threatware).  The threat model at this stage should NOT be approved as an approval needs to be added to the threat model document itself by an approver.
- When an approver has reviewed a threat model, and added their approval (which involves ensuring the `Current Version` and `Approved Version` of the threat model match, and that the corressponding row in the `Version history` table has been populated with the `Approver's Name` and `Approval Date`), then the approver can submit the threat model using `manage.submit`.  This submits the threat model for aproval to the management data storage location i.e. by default the storage location is a git repo, and this creates a new branch with name equalling the threat model ID, if the approver is happy to approve they merge the branch to the `approved` branch.

Both of these use cases apply to when a threat model is created, and everytime it needs to be updated.

`manage.submit` takes the following parameters:
- `scheme` - the scheme name of the scheme required to parse the submitted threat model.
- `docloc` - the document ID of the threat model document.

threatware will confirm that the `scheme` and `docloc` refer to a threat model known to the management data storage location i.e. that `create` for the same `scheme` and `docloc` had been previously invoked, and whether the version of the threat model being submitted is already considered approved or not (threatware does not support re-approving the same threat model version i.e. approvals are final (at least via threatware, things can be changed directly in the storage location)).

Examples:

Using `manage.submit` with threatware as a lambda, to submit a threat model for approval, for a threat model document in Confluence:

    https://<lambda-url>/threatware?action=manage.submit&scheme=confluence_1.0&docloc=123456

Using `manage.create` threatware as a CLI, to submit a threat model for approval, for a threat model document in Google Docs:

    python3 -m actions.handler manage submit -scheme googledoc_1.0 -docloc 123456

Note, when using the CLI we pass in `submit` as a sub-command to `manage` i.e. `manage submit` (note the space separating them, not a `.`).

## manage.check

The purpose of `manage.check` is to allow a threat model author to check whether a change they have made to their existing threat model requires re-approval.  This is convenience action to make a threat modelling programme scale better (the idea being the small set of threat model approvers will not have to spend time approving minro changes to threat models), but it's not necessary to use this action to benefit from threatware's other `manage` actions.

How exactly threatware determines whether or not a change to a threat model requires re-approval is entirely configurable.  By default i.e. using `confluence_1.0` or `googledocs_1.0` `scheme`, threatware is looking for new threats or new controls in the updated threat model.  Specifically it is looking for any differences between the current version of the threat model and the last approved version of the threat model (the last approved version is stored in management data storage location).

Note, it is assumed that the threat model author will run `verify` on an updated threat model, and address any issues raised, before using the `manage.check` action (as although by default threatware is looking just at new threats/controls, `verify` will ensures new threats/controls must be added for any changes to components or assets).

The goal of `manage.check` is not to perfectly determine if changes to a threat model require re-approval, but it will be useful in cases where the threat model author; adds a new out-of-scope component, or adds a new asset that is stored in the same location as existing assets.  `manage.check` is trying to avoid re-approvals for situations where a change is very unlikely to impact security.  

`manage.check` is configured with a maximum age for a threat model as well though (by default 365 days), and any change to a threat model when it has been greater than the maximum age since the threat model was approved, will require re-approval.

`manage.check` takes the following parameters:
- `scheme` - the scheme name of the scheme required to parse the current version of the threat model.
- `docloc` - the document ID of the threat model document.

Examples:

Using `manage.check` with threatware as a lambda, to submit a threat model for a re-approval check, for a threat model document in Confluence:

    https://<lambda-url>/threatware?action=manage.check&scheme=confluence_1.0&docloc=123456

Using `manage.create` threatware as a CLI, to submit a threat model for a re-approval check, for a threat model document in Google Docs:

    python3 -m actions.handler manage check -scheme googledoc_1.0 -docloc 123456

Note, when using the CLI we pass in `check` as a sub-command to `manage` i.e. `manage check` (note the space separating them, not a `.`).

## manage.indexdata

The purpose of `manage.indexdata` is to return the current index metadata stored for a threat model, primarily as a convenience method to determine what version (if any) of a threat model with a given threat model ID, is approved or not.  It can also be used to retrieve the `scheme` and `docloc` for the threat model when only it's threat model ID is known.

`manage.indexdata` takes the following parameters:
- `id` - the threat model ID (e.g. `CMP.TMD.4`) to retrieve index metadata for

Examples:

Using `manage.indexdata` with threatware as a lambda, to request index metadata for a threat model document:

    https://<lambda-url>/threatware?action=manage.indexdata&id=CMP.TMD.4

Using `manage.indexdata` threatware as a CLI, to submit to request index metadata for a threat model:

    python3 -m actions.handler manage indexdata -id CMP.TMD.4

Note, when using the CLI we pass in `indexdata` as a sub-command to `manage` i.e. `manage indexdata` (note the space separating them, not a `.`).