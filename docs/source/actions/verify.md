# verify

The purpose of `verify` is to detect verification errors in your threat model document.  

The `verify` actions allows:
- uses who are not experts at creating threat models to get feedback on a partially complete threat model document, telling them about issues that need to be resolved before a threat model should be submitted for approval
- an approver of a threat model to get a degree (but not complete) assurance that a threat model has been populated and is free of various common mistakes/omissions/errors

## Parameters 

`verify` takes the following parameters

- `scheme` - the scheme name to use.  This defines how to convert the threat model document to the model format.
- `docloc` - the document ID of the threat model document (in the document location (e.g. Confluence, Google Doc) specified by `scheme`)
- `doctemplate` - the document ID of the threat model template document (in the document location (e.g. Confluence, Google Doc) specified by `scheme`)
- `reports` - what reports to return in addition to the verification issues
    - `none` - (the default) do not return any reports
    - `assets` - return a report showing the controls covering each asset per (in-scope) storage location
    - `controls` - return a report showing which assets each control covers per (in-scope) storage location
    - `all` - return all (i.e. `assets` and `controls`) reports

## Examples

### Lambda

Using `verify` with threatware as a lambda, to verify a threat model document in Confluence:

    https://<lambda-url>/threatware?format=html&action=verify&scheme=confluence_1.0&docloc=123456&doctemplate=67890

Note: we only need to pass in the document ID (`docloc=123456`) because the `scheme` parameter is set to `confluence_1.0`, which configures threatware to look for a Confluence page with that ID using the Confluence location and credentials configured for [](../configure/authentication.md)

:::{admonition} Tip
:class: tip
For the `verify` action threatware supports returning an HTML version of the threat model where any errors are highlighted and tooltips are present to describe the error.

It's a much nicer experience (compared to looking through JSON output) and is recommended for anyone using the `verify` action.  However, the `reports` parameter will be ignored when the format is `html`.
:::

### API

Using `verify` with threatware as an API, to verify a threat model document in Confluence:

    https://<api-hostname>/verify?format=html&scheme=confluence_1.0&docloc=123456&doctemplate=67890

Note: we only need to pass in the document ID (`docloc=123456`) because the `scheme` parameter is set to `confluence_1.0`, which configures threatware to look for a Confluence page with that ID using the Confluence location and credentials configured for [](../configure/authentication.md)


### CLI

Using `verify` threatware as a CLI, to verify a threat model document in Google Docs:

    python3 -m actions.handler verify -scheme googledoc_1.0 -docloc 123456 -doctemplate 67890 -reports all

Note: we only need to pass in the document ID (`docloc=123456`) because the `scheme` parameter is set to `googledoc_1.0`, which configures threatware to look for a Google Document with that ID using the Google credentials configured for [](../configure/authentication.md)

Practically, you'll likely want to redirect the output of the command to a file to review the results e.g.

    python3 -m actions.handler verify -scheme googledoc_1.0 -docloc 123456 -doctemplate 67890 -reports all > results.json
or

    python3 -m actions.handler -f html verify -scheme googledoc_1.0 -docloc 123456 -doctemplate 67890 > results.html
