# Threats and Controls

If you have been following [](./overview.md#the-threat-modelling-process) then ideally you have already noted some threats and controls in the Threats and Controls Table, but otherwise you may feel like you have only have gathered a bunch of information about the system you are threat modelling; a description and use cases, references, all the in- and out-of-scope components, identities, authentication and authorisation mechanisms, the functional and technical assets, diagrams, operational security controls.  It may seem odd that only now you are getting to call out threats!  

The good news is that you have already gathered the vast majority of information you need in order to populate the Threats and Controls Table, and populating the table is more about aggregating the information you have collected and presented it concisely in a single place.

## Threats and Controls Table

Populating the threats and controls table is done by going through the information already gathered (bearing in mind populating a threat model is iterative, so you may have to do this more than once), and extracting and aggregating the threats, listing any existing controls, and creating work tickets to investigate further mitigations if required.

To populate the Threats and Controls Table with the information you have so far:
- go through the [](./components.md#components-authn-and-authz-table) and look for threats relating to missing authentication or authorization
- go through the [](./assets.md#technical-assets-table) and the [](./assets.md#functional-assets-table) and capture a threat `Unauthorized access to ...` for each of the "storage types" (pre-populated storage locations in the template) in the `Storage Location` column
- go through the [](./assets.md#technical-assets-table) and the [](./assets.md#functional-assets-table) and capture a threat `Unauthorized access to ...` for each of the in-scope Components in the `Storage Location` column
- go through the [](./operations.md#operational-security-table) and capture any threats for any processes that are missing or not following good security practices

For each of the above also capture any existing controls.  Any controls the help mitigate threats in different rows should be repeated (cut & paste) per row.

Now is a good time to go through the list of "Controls (Existing)" captured so far and to review them for any known controls that are missing.  The team has likely implemented some security controls and so we need to make sure they have all been captured (remembering that they should only be for in-scope components and relate to the specific environment in-scope as well).  Any controls that haven't been captured should first try to find a home against existing threats, but if no existing threats are suitable, then threats should be added so the control can be captured (this may lead to updating other tables).

After completing the above you should have captured the majority of threats facing the assets in the system being threat modelled.  But there are some more ways to uncover other threats:
- go through the tech stack of the in-scope components and try to identify any that should following specific security or hardening guidelines, and capture threats that these components may not be following the guidelines
:::{admonition} Tip
The control to ensure a technology is follow best practice security guidelines is often to introduce a security tool that can automate such checks.  Raising this threat is a great way to link threat models to any initiatives the Security Team has about introducing tooling.
:::
- go through the tech stack of the in-scope components and try to identify any that are susceptable to common or well-known types of attacks, using a industry vulnerability list e.g. [OWASP TopTen](https://owasp.org/www-project-top-ten/), [SANS Top 25](https://www.sans.org/top25-software-errors/).  Examples might be SQL Injection for databases, or XSS for web servers.  Capture threats for these classes of vulnerabilities
- go through any [](./diagrams.md#sequence-diagrams) looking for positions in the sequence where out of order requests could be made to in-scope components, and work with the team who owns the system to understand if there are any security consequences.  If any are discovered capture these as threats.

The above covers what to put in the Threats and Controls Table, but not how, which is covered below, for each of the columns in the table:

Component(s)
:  A comma or newline separated list of components to which both the asset, threat and control apply.  The value must match a Name from the [](./components.md#components-details-table)

Asset(s)
:  A comma or newline separated list of assets to which both the component, threat and control apply.  The value must match a Name or Category from either the [](./assets.md#functional-assets-table) or the [](./assets.md#technical-assets-table)
:  This can also be an expression that covers all assets in a particular "storage type" or Component.  Possible expressions include (but this is configurable):
   - `All assets stored in `
   - `All assets stored in component - `
   - `All assets stored in location - `

   The expression should end in a named "storage type" or Component e.g. for a storage type of `Environment Variables` the expression would be `All assets stored in Environment Variables`.  The value at the end of the expression must be listed in the Storage Location column of either the [](./assets.md#functional-assets-table) or the [](./assets.md#technical-assets-table).

Threat
:  A brief description of the threat that applies to all the components and assets listed in the row.

:::{admonition} Common mistake
:class: warning
There can only be ONE threat entered in the Threat column for any row.  This ensures it is clear which components and assets the threat applies, and which controls help mitigate the threat.  

To help enforce this threatware will raise an error if it finds a newline in a threat entered.
:::

Controls (Existing)
:  A newline separated brief description of controls that help mitigate the threat as it relates to the components and assets.  Controls that mitigate multiple threats should be repeated on each row they apply (and be exact copies of each other).

Tickets
:  Each row in the Threats and Control Table must be reviewed to determine if the existing controls sufficiently mitigate the threat as it relates to the components and assets.  This must (at least) be done be the approver of the threat model, and can follow any procedure the business already uses, or can be as simple as deciding if there are sensible controls that haven't been implemented but should be.  There is usually an amount of subjectivity to this process, but that is nature of most risk assessment.  For any threat that is not adequately mitigated a ticket (in whatever work tracking system e.g. Jira, that your business uses) should be created, and the ticket identifier (hyperlinked to the work tracking system) value should be placed in this column.  Multple tickets can be newline separated.  

   :::{admonition} Tip
   The threatware `verify` action also provides 2 reports, as `asset-coverage-report` and a `control-coverage-report`.

   The `asset-coverage-report` parses the Threats and Controls Table and returns a list of all assets, and for each assets it lists all the threats that apply to that asset (even for assets that are part of an aggregate expression).  This can be used to review threats per asset and decide if any asset is missing threats.

   The `control-coverage-report` parses the Threats and Controls Table and returns a list of all locations and assets in those locations, to which the control helps mitigate a threat to those assets.  This can be used determine which controls are heavily relied on (because they protect numerous assets), and might warrant closer review.
   :::

   The ticket created need not be the specific control that should be implmented (although that may be appropriate sometimes), but can just be a ticket to more formally review the risk concern raised by the threat, which can then decide if the risk needs to be mitigated further and the possible controls (preventative, detective, etc) that could be implemented to do so.