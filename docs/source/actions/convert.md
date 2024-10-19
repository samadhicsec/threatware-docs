# convert

The purpose of the `convert` action is to convert a threat modelling document to a model of the document, according to a scheme.  The model is the common format of the document, only containing relevant information, that other actions operate on.

Common uses of the `convert` action include:
- Verifying/debugging the scheme definition is correct by manual inspection of the output of `convert` (a.k.a a model of the document)
- Determining if all appropriate information in the threat model is being captured (as the output of `convert` is stored by threatware's `manage` actions)
- To capture the model of the threat modelling document for manually putting in storage
- To feed the model of the threat modelling document to some other process

## Parameters 

`convert` takes the following parameters

- `scheme` - the scheme name to use.  This defines how to convert the threat model document to the model format.
- `docloc` - the document ID of the threat model document (in the document location specified by `scheme`)
- `meta`   - defines which meta data should be captured in the output model.  The output model is just a hierarchy of key/value pairs.  They keys have associated metadata e.g. a tag indicating how to validate the value. Possible values are:
    - `none`       - the output model will contain no additional metadata relating to the keys.  This is useful for capturing just the data of a threat model (with no threatware specific key metadata), which is useful for passing to other processes, or to be consumed by humans.
    - `tags`       - (default value) the output model will contain the tags that are associated to each key (tags are defined in the scheme file).  This is useful for debugging issues with the scheme definition.
    - `properties` - the output model will contain the tags and properties associated to each key (properties are metadata captured during the coverting of the document).  This is useful for advanced debugging of issues with the scheme definition.  The `properties` value should only be used when the output format parameter is `yaml`, as json is not (natively) capable of complex objects as keys.  This format is a complete internal representation of what threatware uses, and the only format that threatware can consume when a model is stored (relevant for some `manage` actions).

## Examples

### Lambda

Using `convert` with threatware as a lambda to debug a scheme definition, being used on a threat model document in Confluence.  This relies on the default value of `meta` = `tags`:

    https://<lambda-url>/threatware?action=convert&scheme=confluence_1.0&docloc=123456

### API

Using `convert` with threatware as an API to debug a scheme definition, being used on a threat model document in Confluence.  This relies on the default value of `meta` = `tags`:

    https://<api-hostname>/convert?scheme=confluence_1.0&docloc=123456

### CLI

Using `convert` threatware as a CLI to generate a human readable version of a threat model document in Google Docs

    python3 -m actions.handler convert -scheme googledoc_1.0 -docloc 123456 -meta none