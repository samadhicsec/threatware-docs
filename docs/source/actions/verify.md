# verify

The purpose of `verify` is to detect verification errors in your threat model document.  

The `verify` actions allows:
- uses who are not experts at creating threat models to get feedback on a partially complete threat model document, telling them about issues that need to be resolved before a threat model should be submitted for approval
- an approver of a threat model to get a degree (but not complete) assurance that a threat model has been populated and is free of various common mistakes/omissions/errors

`verify` takes the following parameters

- `scheme` - the scheme name to use.  This defines how to convert the threat model document to the model format.
- `docloc` - the document ID of the threat model document (in the document location (e.g. Confluence, Google Doc) specified by `scheme`)
- `doctemplate` - the document ID of the threat model template document (in the document location (e.g. Confluence, Google Doc) specified by `scheme`)
- `reports` - what reports to return in addition to the verification issues
    - `none` - (the default) do not return any reports
    - `assets` - return a report showing the controls covering each asset per (in-scope) storage location
    - `controls` - return a report showing which assets each control covers per (in-scope) storage location
    - `all` - return all (i.e. `assets` and `controls`) reports

Examples:

Using `verify` with threatware as a lambda, to verify a threat model document in Confluence:

    https://<lambda-url>/threatware?action=verify&scheme=confluence_1.0&docloc=123456&doctemplate=67890&reports=all

Note: because the scheme `confluence_1.0` has been specified, threatware will access the document with ID `123456` in the configured Confluence location.

Using `verify` threatware as a CLI, to verify a threat model document in Google Docs:

    python3 -m actions.handler verify -scheme googledoc_1.0 -docloc 123456 -doctemplate 67890 -reports all

Note: because the scheme `googledoc_1.0` has been specified, threatware will access the Google document with ID `123456`.