# measure

The purpose of `measure` is to determine the "distance" (i.e. how far apart) a threat model is from it's template.  It can actually be used to determine how far apart any 2 threat models are, but the original use case is the distance of a threat model to it's template.

The scenario imagined where this use case is applicable is when a threat modelling programme has matured to the point where teams are creating specialised threat model templates that are pre-populated with components, assets, threats & controls that are specific to the technology stacks and systems in common usage across that team.  Any new system to be threat modelled that is based on the same technology stacks and systems, should be simple to create a threat model for because the additional information required to be added to the template (the new threat model will start as a copy of the template) should be minor.  In some sense the distance between the new threat model and the template is "small".  `measure` can be used to aid in a risk assessment of the new system being threat modelled, as if it returns a "small" distance then the new system is using mostly familiar technology stacks and systems, and it might be reasonable to assume then that the security properties of new system are not novel.  On the other hand, if `measure` returns a "large" distance, then that implies potentially many new technology stacks and systems are involved in this new system, which means the security properties of new system are likely novel, and so should be a priority for security review.

How exactly `measure` determines the distance between a threat model and its template is entirely configurable.  By default i.e. using `confluence_1.0` or `googledocs_1.0` `scheme`, threatware is looking for:
- new 3rd party services
- new internal services
- new authentication and authorisation methods (as a pair)
- new threats and controls

## Parameters

`measure` takes the following parameters:

- `scheme` - the scheme name to use.  This defines how to convert the threat model document and template to the model format.
- `docloc` - the document ID of the threat model document (in the document location specified by `scheme`)
- `doctemplate` - the document ID of the threat model template document (in the document location specified by `scheme`)

## Examples

### Lambda

Using `measure` with threatware as a lambda, to measure the distance between a threat model document and a threat model template in Confluence:

    https://<lambda-url>/threatware?action=measure&scheme=confluence_1.0&docloc=123456&doctemplate=67890

### API

Using `measure` with threatware as an API, to measure the distance between a threat model document and a threat model template in Confluence:

    https://<api-hostname>/measure?scheme=confluence_1.0&docloc=123456&doctemplate=67890

### CLI

Using `measure` threatware as a CLI, to measure the distance between a threat model document and a threat model template in Google Docs:

    python3 -m actions.handler measure -scheme googledoc_1.0 -docloc 123456 -doctemplate 67890