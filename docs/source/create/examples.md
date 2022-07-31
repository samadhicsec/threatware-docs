# Example

It would be ironic for a threat modelling tool to not have its own threat model, and so that is the primary example shared here.

Before sharing the finished threat model it will be useful to share a partially completed threat model, which before continuing you should review - [Threatware Threat Model - Incomplete](https://docs.google.com/document/d/1NQepy_K4tKcIT9xpssRDcW4T58uk_slGbwafN307rWQ/edit?usp=sharing)

This incomplete threat model is useful to demonstrate 2 things
1) For someone reviewing the threat model they may very well see it as being mostly complete, if not actually complete.
2) The benefit of using threatware's `verify` action can be seen, as it highlights the threats that are missing (the syntax of the threat model is otherwise fine, so there no errors of that type reported)

Below we can see the output threatware `verify` on the incomplete threat model:

```json
{
  "result": "Information",
  "description": "The threat model is not valid",
  "details": {
    "issues": [
      {
        "type": "ERROR",
        "table": "In Threats and Controls Table",
        "error-description": "No threat was found in the 'Threats and Controls Table' that covered the asset 'Threat model YAML' (from the 'Functional Assets Table') when stored in location 'Client Temp Storage'.",
        "fix-description": "The Threats and Controls Table must include a row where the 'Asset(s)' column includes one of; the asset name i.e. 'Threat model YAML', the asset category i.e. 'Functional Data', or text referencing (see fix data) the storage location i.e. 'Client Temp Storage'",
        "fix-data": [
          "All assets stored in ",
          "All assets stored in component - ",
          "All assets stored in location - "
        ],
        "verifier": "coverage-validation"
      },
      {
        "type": "ERROR",
        "table": "In Threats and Controls Table",
        "error-description": "No threat was found in the 'Threats and Controls Table' that covered the asset 'Threat model index data' (from the 'Functional Assets Table') when stored in location 'Client Temp Storage'.",
        "fix-description": "The Threats and Controls Table must include a row where the 'Asset(s)' column includes one of; the asset name i.e. 'Threat model index data', the asset category i.e. 'Functional Data', or text referencing (see fix data) the storage location i.e. 'Client Temp Storage'",
        "fix-data": [
          "All assets stored in ",
          "All assets stored in component - ",
          "All assets stored in location - "
        ],
        "verifier": "coverage-validation"
      },
      {
        "type": "ERROR",
        "table": "In Threats and Controls Table",
        "error-description": "No threat was found in the 'Threats and Controls Table' that covered the asset 'Threat Model version history data' (from the 'Functional Assets Table') when stored in location 'Client Temp Storage'.",
        "fix-description": "The Threats and Controls Table must include a row where the 'Asset(s)' column includes one of; the asset name i.e. 'Threat Model version history data', the asset category i.e. 'Functional Data', or text referencing (see fix data) the storage location i.e. 'Client Temp Storage'",
        "fix-data": [
          "All assets stored in ",
          "All assets stored in component - ",
          "All assets stored in location - "
        ],
        "verifier": "coverage-validation"
      },
      {
        "type": "ERROR",
        "table": "In Threats and Controls Table",
        "error-description": "No threat was found in the 'Threats and Controls Table' that covered the asset 'threatware config files' (from the 'Technical Assets Table') when stored in location 'CLI Configuration'.",
        "fix-description": "The Threats and Controls Table must include a row where the 'Asset(s)' column includes one of; the asset name i.e. 'threatware config files', the asset category i.e. 'Configuration', or text referencing (see fix data) the storage location i.e. 'CLI Configuration'",
        "fix-data": [
          "All assets stored in ",
          "All assets stored in component - ",
          "All assets stored in location - "
        ],
        "verifier": "coverage-validation"
      },
      {
        "type": "ERROR",
        "table": "In Threats and Controls Table",
        "error-description": "No threat was found in the 'Threats and Controls Table' that covered the asset 'threatware config files' (from the 'Technical Assets Table') when stored in location 'ACS'.",
        "fix-description": "The Threats and Controls Table must include a row where the 'Asset(s)' column includes one of; the asset name i.e. 'threatware config files', the asset category i.e. 'Configuration', or text referencing (see fix data) the storage location i.e. 'ACS'",
        "fix-data": [
          "All assets stored in ",
          "All assets stored in component - ",
          "All assets stored in location - "
        ],
        "verifier": "coverage-validation"
      },
      {
        "type": "ERROR",
        "table": "In Threats and Controls Table",
        "error-description": "No threat was found in the 'Threats and Controls Table' that covered the asset 'repo branch names' (from the 'Technical Assets Table') when stored in location 'CLI Configuration'.",
        "fix-description": "The Threats and Controls Table must include a row where the 'Asset(s)' column includes one of; the asset name i.e. 'repo branch names', the asset category i.e. 'Configuration', or text referencing (see fix data) the storage location i.e. 'CLI Configuration'",
        "fix-data": [
          "All assets stored in ",
          "All assets stored in component - ",
          "All assets stored in location - "
        ],
        "verifier": "coverage-validation"
      },
      {
        "type": "ERROR",
        "table": "In Threats and Controls Table",
        "error-description": "No threat was found in the 'Threats and Controls Table' that covered the asset 'repo branch names' (from the 'Technical Assets Table') when stored in location 'ACS'.",
        "fix-description": "The Threats and Controls Table must include a row where the 'Asset(s)' column includes one of; the asset name i.e. 'repo branch names', the asset category i.e. 'Configuration', or text referencing (see fix data) the storage location i.e. 'ACS'",
        "fix-data": [
          "All assets stored in ",
          "All assets stored in component - ",
          "All assets stored in location - "
        ],
        "verifier": "coverage-validation"
      },
      {
        "type": "ERROR",
        "table": "In Threats and Controls Table",
        "error-description": "No threat was found in the 'Threats and Controls Table' that covered the asset 'Confluence API key' (from the 'Technical Assets Table') when stored in location 'CLI Configuration'.",
        "fix-description": "The Threats and Controls Table must include a row where the 'Asset(s)' column includes one of; the asset name i.e. 'Confluence API key', the asset category i.e. 'Authentication Credentials', or text referencing (see fix data) the storage location i.e. 'CLI Configuration'",
        "fix-data": [
          "All assets stored in ",
          "All assets stored in component - ",
          "All assets stored in location - "
        ],
        "verifier": "coverage-validation"
      },
      {
        "type": "ERROR",
        "table": "In Threats and Controls Table",
        "error-description": "No threat was found in the 'Threats and Controls Table' that covered the asset 'Google Docs API key' (from the 'Technical Assets Table') when stored in location 'CLI Configuration'.",
        "fix-description": "The Threats and Controls Table must include a row where the 'Asset(s)' column includes one of; the asset name i.e. 'Google Docs API key', the asset category i.e. 'Authentication Credentials', or text referencing (see fix data) the storage location i.e. 'CLI Configuration'",
        "fix-data": [
          "All assets stored in ",
          "All assets stored in component - ",
          "All assets stored in location - "
        ],
        "verifier": "coverage-validation"
      },
      {
        "type": "ERROR",
        "table": "In Threats and Controls Table",
        "error-description": "No threat was found in the 'Threats and Controls Table' that covered the asset 'Management repo default branch' (from the 'Technical Assets Table') when stored in location 'CLI Configuration'.",
        "fix-description": "The Threats and Controls Table must include a row where the 'Asset(s)' column includes one of; the asset name i.e. 'Management repo default branch', the asset category i.e. 'Authorisation configuration', or text referencing (see fix data) the storage location i.e. 'CLI Configuration'",
        "fix-data": [
          "All assets stored in ",
          "All assets stored in component - ",
          "All assets stored in location - "
        ],
        "verifier": "coverage-validation"
      },
      {
        "type": "ERROR",
        "table": "In Threats and Controls Table",
        "error-description": "No threat was found in the 'Threats and Controls Table' that covered the asset 'Management repo default branch' (from the 'Technical Assets Table') when stored in location 'ACS'.",
        "fix-description": "The Threats and Controls Table must include a row where the 'Asset(s)' column includes one of; the asset name i.e. 'Management repo default branch', the asset category i.e. 'Authorisation configuration', or text referencing (see fix data) the storage location i.e. 'ACS'",
        "fix-data": [
          "All assets stored in ",
          "All assets stored in component - ",
          "All assets stored in location - "
        ],
        "verifier": "coverage-validation"
      },
      {
        "type": "ERROR",
        "table": "In Threats and Controls Table",
        "error-description": "No threat was found in the 'Threats and Controls Table' that covered the asset 'Git Configuration Repo permissions' (from the 'Technical Assets Table') when stored in location 'Git Configuration Repo'.",
        "fix-description": "The Threats and Controls Table must include a row where the 'Asset(s)' column includes one of; the asset name i.e. 'Git Configuration Repo permissions', the asset category i.e. 'Authorisation configuration', or text referencing (see fix data) the storage location i.e. 'Git Configuration Repo'",
        "fix-data": [
          "All assets stored in ",
          "All assets stored in component - ",
          "All assets stored in location - "
        ],
        "verifier": "coverage-validation"
      },
      {
        "type": "ERROR",
        "table": "In Threats and Controls Table",
        "error-description": "No threat was found in the 'Threats and Controls Table' that covered the asset 'All URLs of components stored in config files' (from the 'Technical Assets Table') when stored in location 'CLI Configuration'.",
        "fix-description": "The Threats and Controls Table must include a row where the 'Asset(s)' column includes one of; the asset name i.e. 'All URLs of components stored in config files', the asset category i.e. 'Locations', or text referencing (see fix data) the storage location i.e. 'CLI Configuration'",
        "fix-data": [
          "All assets stored in ",
          "All assets stored in component - ",
          "All assets stored in location - "
        ],
        "verifier": "coverage-validation"
      },
      {
        "type": "ERROR",
        "table": "In Threats and Controls Table",
        "error-description": "No threat was found in the 'Threats and Controls Table' that covered the asset 'Git Configuration Repo Location' (from the 'Technical Assets Table') when stored in location 'Lambda Environment Variables'.",
        "fix-description": "The Threats and Controls Table must include a row where the 'Asset(s)' column includes one of; the asset name i.e. 'Git Configuration Repo Location', the asset category i.e. 'Locations', or text referencing (see fix data) the storage location i.e. 'Lambda Environment Variables'",
        "fix-data": [
          "All assets stored in ",
          "All assets stored in component - ",
          "All assets stored in location - "
        ],
        "verifier": "coverage-validation"
      },
      {
        "type": "ERROR",
        "table": "In Threats and Controls Table",
        "error-description": "No threat was found in the 'Threats and Controls Table' that covered the asset 'CLI Configuration Location' (from the 'Technical Assets Table') when stored in location 'Shell Environment Variables'.",
        "fix-description": "The Threats and Controls Table must include a row where the 'Asset(s)' column includes one of; the asset name i.e. 'CLI Configuration Location', the asset category i.e. 'Locations', or text referencing (see fix data) the storage location i.e. 'Shell Environment Variables'",
        "fix-data": [
          "All assets stored in ",
          "All assets stored in component - ",
          "All assets stored in location - "
        ],
        "verifier": "coverage-validation"
      },
      {
        "type": "ERROR",
        "table": "In Threats and Controls Table",
        "error-description": "No threat was found in the 'Threats and Controls Table' that covered the asset 'Log Data' (from the 'Technical Assets Table') when stored in location 'Cloudtrail'.",
        "fix-description": "The Threats and Controls Table must include a row where the 'Asset(s)' column includes one of; the asset name i.e. 'Log Data', the asset category i.e. 'Audit Data', or text referencing (see fix data) the storage location i.e. 'Cloudtrail'",
        "fix-data": [
          "All assets stored in ",
          "All assets stored in component - ",
          "All assets stored in location - "
        ],
        "verifier": "coverage-validation"
      }
    ]
  },
  "request": {
    "action": "verify",
    "scheme": "googledoc_1.0",
    "docloc": "1PwszXLMnm7eEAaCx8dOPetQ3Gx_snWnZq6L7dZZ5L5Q",
    "doctemplate": "1DBskRZBKpolIchljkVowFsvB-xRlSVf8sPguOnxsnhU",
    "format": "json",
    "reports": "none"
  }
}
```

threatware `verify` has identified 15 assets that were not covered by a threat in the Threats and Controls table.

:::{admonition} Common Misconception
:class: warning
It's tempting to conclude that threatware `verify` has identicated there are 15 missing threats, but this incorrect.

As can be seen from the `fix-data` in the `verify` response, we would expect a threat to cover multiple assets.  Take for example the first 2 ERRORS in the findings which mention assets `Threat model YAML` and `Threat model index data` which both are stored in component `Client Temp Storage` - we would absolutely expect the same threats and controls to apply to both assets as they are in the same location (obviously that is not always true, but it is often true).  This means we only want to add 1 new row to the Threats and Controls table to cover both of these assets, and threatware allows this by either listing both assets, or using the language in the `fix-data` section.

Ultimately only 6 new rows needed to be added to the Threats and Controls table to cover the 15 assets missing a covering threat that `verify` reported.
:::

The finished threat model for threatware can be found - [Threatware Threat Model](https://docs.google.com/document/d/1PwszXLMnm7eEAaCx8dOPetQ3Gx_snWnZq6L7dZZ5L5Q/edit?usp=sharing)