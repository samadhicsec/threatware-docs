# Common and Shared Parameters

## Common Parameters

Many of the actions that threatware supports takes common parameters, which are described here:

### scheme

`scheme` is the name of the scheme to be used to parse the threat modelling document.  A scheme is like a schema e.g. XML schema.

The possible `scheme` values are located in the `schemes/schemes.yaml` file.  The value to use is the name (yaml key), not the file name (yaml value).

The `scheme` values provided by default are:

- `confluence_1.0`
- `googledoc_1.0`

At the top of each `scheme` files is a `document-storage` setting that tells threatware what document storage location to connect to.

For example:
1. When the `scheme` parameter is set to `googledoc_1.0` threatware will look at the `schemes/schemes.yaml` configuration to find the corresponding scheme file to use e.g. `googledoc-scheme-1.0.yaml`
1. threatware will open `googledoc-scheme-1.0.yaml` and read the `document-storage` yaml key, which in this case has the value `googledoc`
1. threatware internally knows that a storage location of `googledoc` means it will use the configuration for `google` in `providers/providers_config.yaml` (for the appropriate environment e.g. lambda, cli) in order to authenticate to the Google APIs and retrieve the threat model document (given the ID of the document, see `docloc` below)

### docloc and doctemplate

The `docloc` and `doctemplate` parameters are the document IDs of the document relative to its storage location (note, a document ID is different to a threat model ID).  The storage location is determined from the `scheme` parameter.

For instance, if your `scheme` parameter was `confluence_1.0` and your `docloc` parameter was `123456` then threatware would try to retrieve the document with ID `123456` from the configured Confluence server.  If you changed the `scheme` to `googledoc_1.0` then threatware would try to retrieve the document with ID `123456` from Google Docs.

#### Confluence document IDs

The document ID for Confluence pages varies by Confluence server type.  Often it is present in the URL of a page, e.g.

    https://threatmodels.atlassian.net/wiki/spaces/TM/pages/31653889/Threat+Model+1

For the above Confluence page, the document ID is `31653889`.

Sometimes the document ID is not present in the URL of the page, when this is the case it is usually present in the URL of the 'Edit' Confluence page i.e. right-click the Edit button and 'Copy Link', e.g.

    https://threatmodels.atlassian.net/wiki/spaces/TM/pages/edit-v2/31653889

#### Google Doc document IDs

The document ID for a Google Doc is the long random looking value in the URL of the document e.g.

    https://docs.google.com/document/d/1h3GsOlikDyQkdzE2JLRsjz2pYAT7PoEwJcORxqGyh2Y/edit?

For the above Google Doc the document ID is `1h3GsOlikDyQkdzE2JLRsjz2pYAT7PoEwJcORxqGyh2Y`.

## Shared Parameters

The following are parameters that can be specified and are independent of action

### format

threatware supports output in either `json` (the default), `yaml` or `html` (just for the `verify` action).

Example:

    python3 -f yaml -m actions.handler convert -scheme googledoc_1.0 -docloc 123456 -meta properties

### lang

threatware supports localisation and will accept a language code representing the language to output in.

*Whilst different languages are supported, threatware currently provides a single language, English*

Example:

    python3 -l en-US -f yaml -m actions.handler convert -scheme googledoc_1.0 -docloc 123456 -meta properties