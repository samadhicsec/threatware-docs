# Scheme File Definition

## How to Define a scheme for a Threat Model Document

### Overview

threatware tries to be format agnostic for the structure of the threat model document.  This means you can structure your threat model how you want.  In order to support this, threatware needs a file (called a 'scheme') that represents the format of your threat model document.  This is exactly how the [default template](../create/template.md) works, and you can see the [default 'scheme' for Confluence and Google Docs](https://github.com/samadhicsec/threatware-config/tree/main/schemes) to look at as examples.

The 'scheme' is a parameter that is passed to threatware actions, and is the basis for the `convert` action to convert a threat model document to a `yaml` representation (which then becomes the common format that all other actions use for processing).

Unfortunately, there is no standardised language to describe the format of a generic document and assign attibutes to parts of it.  Standard document formats like HTML or Markdown aren't expressive enough to allow capturing detailed information that might be nested in a document, and other schema langauges are specific to their corressponding format e.g. XSD for XML.  So threatware uses a custom language to describe threat model documents - which is by no means an ideal solution.

The goal of this section is to give you a high level overview of the format of 'scheme' files and provide an example of how to extract a table from a Google Doc.  Whilst it isn't expected most people will want to create 'scheme' files from scratch, the idea is to explain the basics, which should allow modifications of existing 'scheme' files.

### Scheme format (high-level)

The job of the scheme format is to map the contents of a document to a `yaml` representation of that document.  The `yaml` representation does not need to include all the information in the document, just the information you want to store, or you want to validate (and some information like diagrams cannot currently be captured).

The 'scheme' file itself is a `yaml` file and at the highest level a scheme document looks like:

```{code-block} yaml
:linenos:
---
scheme:
  map:
    get-data:
    map-data:
    output-data:
```

It's helpful to think of threatware as having an internal document conversion process that is consuming this configuration, starting with `get-data:`, then taking the result and passing it to `map-data:`, and then taking the result and passing it to `output-data:`.

Where
:::{list-table}
:widths: auto 
* - ```{code-block} yaml
    :emphasize-lines: 3
    :lineno-start: 2
    scheme:
      map:
        get-data:
    ```
  - Configures where in the document to get data from.  This data will be passed as input to the processing of the `map-data:` configuration.
* - ```{code-block} yaml
    :emphasize-lines: 1
    :lineno-start: 5
        map-data:
    ```
  - Configures how to map the data from `get-data:` to `yaml` key/value pairs.
* - ```{code-block} yaml
    :emphasize-lines: 1
    :lineno-start: 6
        output-data:
    ```
  - Configures any data processing to perform on the key/value pairs output by `map-data:` (usually some form of post-processing).
:::

Notably, these 3 configurations can be used recursively under a child key of the `map-data:` configuration, which allows us to create arbitrarily nested `yaml` (explained more later) to represent the data in the document.

Now let's add the next level of configuration keys for each of the above:

```{code-block} yaml
:linenos:
:emphasize-lines: 5, 7-10
---
scheme:
  map:
    get-data:
      query:
    map-data:
      - key:
        value:
      - key:
        value:
    output-data:
```

Where:
:::{list-table}
:widths: auto 
* - ```{code-block} yaml
    :emphasize-lines: 2
    :lineno-start: 4
        get-data:
          query:
    ```
  - Will contain the configuration of how to select data from the document.
* - ```{code-block} yaml
    :emphasize-lines: 2-5
    :lineno-start: 6
        map-data:
          - key:
            value:
          - key:
            value:
    ```
  - A list of `key:` / `value:` configurations for how to map data from the output of the `query:` configuration processing to `yaml` key/value pairs.
:::

It'll be easiest to understand the next level of configuration by going through an example of extracting table data from a document.

### Extracting a table

Since a lot of information in documents is often in a table, let's imagine we have a document like the following:

```{admonition} Document
# Threat Model 
## Description
This is a threat model for a series of data flows.
## Threats Table

| Data Flow | Threat Description | Control | Risk Rating |
| --------- | ------------------ | ------- | ----------- |
| DF1       | No use of SSL      | Use TLS | Low |
| DF2       | No encryption      | Use encryption | Low |
| DF3       | Unauthorised access | IP Allowlist | Medium |

## Conclusion

The overall risk is Low.
```

What we want is to extract the information in the table into a `yaml` document that will look like:

```yaml
threats:
  - data-flow: DF1
    threat-description: No use of SSL
    control: Use TLS
    risk-rating: Low
  - data-flow: DF2
    threat-description: No encryption
    control: Use encryption
    risk-rating: Low
  - data-flow: DF3
    threat-description: Unauthorised access
    control: IP Allowlist
    risk-rating: Medium
```

The high level 'scheme' file will start out like this:

```{code-block} yaml
:linenos:
---
scheme:
  version: 1.0
  document-storage: googledoc
  map:
    map-data:
    output-data:
      type: dict
```

Let's explain the new lines, line-by-line:

:::{list-table}
:widths: auto 
* - ```{code-block} yaml
    :emphasize-lines: 2
    :lineno-start: 2
    scheme:
      version: 1.0
    ```
  - This is just the version number of the scheme file format and can only be `1.0` currently.
* - ```{code-block} yaml
    :emphasize-lines: 1
    :lineno-start: 4
      document-storage: googledoc
    ```
  - This tells threatware the document is a Google Doc (`confluence` is currently the only other valid value), and means threatware will export the Google Doc in HTML format in order to process it.
* - ```{code-block} yaml
    :emphasize-lines: 2
    :lineno-start: 7
        output-data:
          type: dict
    ```
  - This tells threatware the content will be output as a `yaml` dictionary (as opposed to a list).
:::

Note, we removed the `get-data:` configuration as that isn't required under the `map:` configuration, because all data will be passed to the rest of the configuration (the job of `get-data:` is to query for a subset of data, but since we want to pass all data we can remove the `get-data:` configuration).

Now let's start specifying how to actual get to the data we want.  Remember at this stage, the entire HTML representation of the Google Doc will be passed to the configuration of `map-data:`.

```{code-block} yaml
:linenos:
:emphasize-lines: 7-13
---
scheme:
  version: 1.0
  document-storage: googledoc
  map:
    map-data:
      - key:
          name: threats
      - value:
          get-data:
            - query:
                type: "html-table"
                xpath: "//html/body/h2[text()='Threats Table']/following::table[1]"
    output-data:
      type: dict
```

Let's explain the new lines, line-by-line:
:::{list-table}
:widths: 50 50 
* - ```{code-block} yaml
    :emphasize-lines: 2-3
    :lineno-start: 6
        map-data:
          - key:
              name: threats
    ```
  - This is the name of the `yaml` key to use.  In this case it will be the root `threats:` key.
* - ```{code-block} yaml
    :emphasize-lines: 1-2
    :lineno-start: 9
          - value:
              get-data:
    ```
  - The `value` configuration defines what value to assign to the above `key:`.  To do this it oftens leverages `get-data:` configuration as a means to extract specific data.  At this stage the whole HTML representation of the Google Doc will be processed by this `get-data:` confgiuration.
* - ```{code-block} yaml
    :emphasize-lines: 1-2
    :lineno-start: 9
                - query:
                    type: "html-table"
    ```
  - This is the type of data we want to extract from the document.  See [](#query-types) for a list of supported types.
* - ```{code-block} yaml
    :emphasize-lines: 1
    :lineno-start: 13
                    xpath: "//html/body/h2[text()='Threats Table']/following::table[1]"
    ```
  - This is the HTML XPath query to the HTML table to get data from.  XPath was chosen as the input is HTML and it is the most compact way to locate an HTML element.  There is a learning curve to using it, but the examples provided should be fairly easy to alter for your own documents.
:::

The above `get-data:` configuration extracts all the data in the table (including the header row), but we still need to assign each row in the table to the list of child keys we want.  To do this we need to add `map-data:` configuration to take the data from `get-data:` and map it to the keys.

```{code-block} yaml
:linenos:
:emphasize-lines: 14-45
---
scheme:
  version: 1.0
  document-storage: googledoc
  map:
    map-data:
      - key:
          name: threats
      - value:
          get-data:
            - query:
                type: "html-table"
                xpath: "//html/body/h2[text()='Threats Table']/following::table[1]"
          map-data:
            - key: 
                name: "data-flow"
              value: 
                get-data:
                  query:
                    type: html-table-row
                    column-num: 0
            - key: 
                name: "threat-description"
              value: 
                get-data:
                  query:
                    type: html-table-row
                    column-num: 1
            - key: 
                name: "control"
              value: 
                get-data:
                  query:
                    type: html-table-row
                    column-num: 2
            - key: 
                name: "risk-rating"
              value: 
                get-data:
                  query:
                    type: html-table-row
                    column-num: 3
          output-data:
            post-processor:
              remove-header-row:
    output-data:
      type: dict
```

Now you can see the recursive nature of the `get-data:` / `map-data:` / `output-data:` configurations, and as we recurse down in the configuration the data queried and mapped at a higher configuration level is passed to the nested configurations.

It's worth repeating that the configuration `get-data:` with `type: "html-table"` is designed to pass 1 row at a time to the subsequent `map-data:` configuration, with the `output-data:` (by default has `type: list`) gathering the output of `map-data:` to a `yaml` list under the `threats` key.

Let's explain the new lines, line-by-line:
:::{list-table}
:widths: auto 

* - ```{code-block} yaml
    :emphasize-lines: 3
    :lineno-start: 14
              map-data:
                - key: 
                    name: "data-flow"
    ```
  - Is going to map some content (defined in `value:` / `get-data:` below) to a `yaml` key called `data-flow`
* - ```{code-block} yaml
    :emphasize-lines: 4
    :lineno-start: 17
              value: 
                get-data:
                  query:
                    type: html-table-row
    ```
  - Is configuration defining the type of data we are processing.  We use `html-table-row` when there is a parent `query:` type that returns an `html-table`
* - ```{code-block} yaml
    :emphasize-lines: 1
    :lineno-start: 21
                    column-num: 0
    ```
  - Is configuration saying get the contents of column 0 in this table row.
:::

The same logic applies to the configuration of each of the 4 list items defined under `map-data:`.  It's also important to note that threatware specifically does not require you to use the name of the column to get content - this was a design choice so that column names could be changed in documents without breaking the document content conversion (but also note that the name of the header above the table is used in the scheme document, so changing that would break document conversion).

Lastly there was:
:::{list-table}
:widths: auto 

* - ```{code-block} yaml
    :emphasize-lines: 2-3
    :lineno-start: 43
              output-data:
                post-processor:
                  remove-header-row:
    ```
  - This configuration strips the header row of the table from the output, as that is not content we want to capture.  Note, this isn't done by default as HTML tables don't always include header rows.
:::

At this stage we have a scheme file sufficiently defined to convert a Google Doc containing a single table into a `yaml` file containing the contents of the table.  However, we don't have enough information to *validate* the contents of the table are correct.  To do that we need to add metadata to the data that we want validate.  To do this in the scheme file format we add a `tags:` configuration.

Let's imagine we want to validate the `data-flow` and `risk-rating` data to make sure it has the correct format.  Also, we want the entry for `control` not to be mandatory (mandatory is the default).

We'll also name our keys, which isn't relevant in this example, but is essential if performing validation between tables.  The scheme format decouples the `key:` / `name:` configuration from the name used to reference content for validation, as this lets us define validation configuration in a language agnostic way (thus supporting internationalization).

```{code-block} yaml
:linenos:
:emphasize-lines: 9-11, 20-22, 30-31, 39-41, 49-51
---
scheme:
  version: 1.0
  document-storage: googledoc
  map:
    map-data:
      - key:
          name: threats
          section: Threats Table
          tags:
            - threats-table-data
      - value:
          get-data:
            - query:
                type: "html-table"
                xpath: "//html/body/h1[text()='Threats Table']/following::table[1]"
          map-data:
            - key: 
                name: "data-flow"
                tags:
                  - data-flow
                  - validate-as-data-flow
              value: 
                get-data:
                  query:
                    type: html-table-row
                    column-num: 0
            - key: 
                name: "threat-description"
                tags:
                  - threat-description
              value: 
                get-data:
                  query:
                    type: html-table-row
                    column-num: 1
            - key: 
                name: "control"
                tags:
                  - control
                  - not-mandatory
              value: 
                get-data:
                  query:
                    type: html-table-row
                    column-num: 2
            - key: 
                name: "risk-rating"
                tags:
                  - risk-rating
                  - validate-as-risk-rating
              value: 
                get-data:
                  query:
                    type: html-table-row
                    column-num: 3
          output-data:
            post-processor:
              remove-header-row:
    output-data:
      type: dict
```

If you look through the scheme format you can see the new `tags:` configuration.  Remember tags don't cause anything to happen during conversion, they are just used by validation logic (so only relevant when the threatware `validate` action is invoked).

Some tags to note:
:::{list-table}
:widths: auto 

* - ```{code-block} yaml
    :emphasize-lines: 3
    :lineno-start: 7
          - key:
              name: threats
              section: Threats Table
    ```
  - Is used to name the table location, and is used when a validation issue is discovered with an element of the table (so it is easier to find the error in the document).
* - ```{code-block} yaml
    :emphasize-lines: 1
    :lineno-start: 22
                      - validate-as-data-flow
    ```
    ```{code-block} yaml
    :emphasize-lines: 1
    :lineno-start: 51
                      - validate-as-risk-rating
    ```
  - These aren't defined, but their definition could be added to [validators_config.yaml](https://github.com/samadhicsec/threatware-config/blob/main/validators/validators_config.yaml), and would mean the validation logic, upon consuming the definition, would look for all key values in the output `yaml` with these tags, and apply the defined validation logic.
:::

```{note}
In practice, writing the `xpath` selectors to get content from HTML can be quite challenging, especially because the output HTML from Google Docs or Confluence contain a lot of additional elements and attributes.  To make this easier, the scheme file format supports a pre-processor that is applied *before* the content gets passed to the root `map:` configuration.  That pre-processor can be used to strip formatting HTML content that otherwise makes extracting data in the HTML challenging.

See the example scheme files [confluence-scheme-1.0.yaml](https://github.com/samadhicsec/threatware-config/blob/main/schemes/confluence-scheme-1.0.yaml) and [googledoc-scheme-1.0.yaml](https://github.com/samadhicsec/threatware-config/blob/main/schemes/googledoc-scheme-1.0.yaml) for appropriate pre-processing values for the corresponding document formats.
```

## Configuring a new scheme file

After you create a new scheme file you need to make it available to use.  To do that you can follow these steps:

1. Save you file in the `schemes/` directory where your configuration files are stored.
1. Update `schemes/schemes.yaml` to include a new key that is the name of your scheme, with a value that is the file location (see the existing extries for examples).
1. Now you can use your new scheme name where ever the [scheme parameter](../actions/parameters.md#scheme) is used.

## Testing a new scheme file

To test the new scheme file created:

- Use the [CLI](../configure/installation.md#cli) version of threatware, for speed of debugging
- Enable [`DEBUG` level logs](../configure/logging.md)
- Use the threatware [convert](../actions/convert.md) action
- Set the `convert` parameter `-meta none` as this will avoid outputting tags, which makes the output easier to read.  Obviously when you add tags to the scheme and want to check the tags are correctly being assigned, then you can remove the the `meta` parameter (as tags are shown by default i.e. `-meta tags`)

## Reference

### Query types

The `get-data:` / `query:` supports the following `type:` values:

:::{list-table}
:widths: auto 
:header-rows: 1

* - Category
  - Type
  - Use Case
  - Example
  - Description
* - HTML
  - `html-table`
  - Extract an HTML table from HTML
  - ```{code-block} yaml
    :emphasize-lines: 3-6
    get-data:
      - query:
          type: "html-table"
          xpath: "//html/body/h1[text()='Details']/following::table[1]"
          remove-header-row:
          remove-rows-if-empty:
    ```
  - This returns the content of an HTML table as a list of rows.  It will iterate over each row, passing it to the associated `map-data:` configuration.  It supports the following configuration
    - `xpath:` - the XPath expression to the table.
    - `remove-header-row:` - if present (no value required) will remove the first row when iterating over the rows to pass to the associated `map-data:` configured.  Generally always better to use the [](./overview.md#post-processing-options) `remove-header-row` instead of this, as that allows threatware to retain metadata about column header names.
    - `remove-rows-if-empty:` - if present (no value required) will remove any empty rows when iterating over the rows to pass to the associated `map-data:` configuration.
* - HTML
  - `html-table-row`
  - Get the value from a column given a row
  - ```{code-block} yaml
    :emphasize-lines: 3-4
    get-data:
      query:
        type: html-table-row
        column-num: 1
    ```
  - This configuration expects to be passed a row from an `html-table` query configuration.  It returns the value from the column number (0 indexed) specified in `column-num`.
* - HTML
  - `html-table-transpose`
  - Get an HTML table as a series of columns
  - ```{code-block} yaml
    :emphasize-lines: 6
    get-data:
      - query:
          type: "html-table"
          xpath: "//html/body/h1[text()='Details']/following::table[1]"
      - query:
          type: "html-table-transpose"
    ```
  - This is usually chained with an `html-table` query, and instead of returning the rows, it returns the transpose of the table meaning the columns are passed to the associated `map-data:` configuration.  This is useful for tables where the headers are in the first column (as opposed to the first row).
* - Text
  - `text-split`
  - Returns individual data in a section of text
  - ```{code-block} yaml
    :emphasize-lines: 6-10
    get-data:
      - query:
          type: html-table-row
          column-num: 2
      - query:
          type: text-split
          split-by:
            char-separators: 
              - ","
              - "\n"
    ```
  - Given a value from a previous query as input, the `text-split` type will split the value and iterate over each result, passing it to the associated `map-data:` configuration.  Possible types of splitting include:
    - `char-separators:` a list of characters, any of which present will split the value into multiple smaller values
    - `line-regex:` a (python) regular expression with group capture (or if not specified the last group is selected).  The input value is split into lines, and the regex run on each line.
* - Text
  - `text-match`
  - Returns lines that match
  - ```{code-block} yaml
    :emphasize-lines: 6-7
    get-data:
      - query:
          type: html-table-row
          column-num: 2
      - query:
          type: text-match
          line-regex: "(?i)confidentiality|integrity|availability"
    ```
  - Given a value from a previous query as input, the `text-match` type will split the value into lines, and run the regex over each line, outputting the entire line if the regex matches.
* - Text
  - `text-replace`
  - Returns a replacement value on match
  - ```{code-block} yaml
    :emphasize-lines: 6-8
    get-data:
      - query:
          type: html-table-row
          column-num: 2
      - query:
          type: text-replace
          match: "SSL"
          replacement: "TLS"
    ```
  - Given a value from a previous query as input, the `text-replace` type will check if the value is an exact match for the `match:` value and if so it will return the `replacement:` value.  If there is no match, the original string is returned.
* - Value
  - `value-extract`
  - Returns a capture group from a regex
  - ```{code-block} yaml
    :emphasize-lines: 3-5
    get-data:
      - query:
          type: value-extract
          regex: "^(\\w+):(.*)"
          group: 1
    ```
  - Given a value from a previous query as input, the `value-extract` type will return the specified capture `group` from the `regex:`.  Note, group 0 matches the whole string if it matches at all, so group 1 is the first group of the regex, etc.
* - Value
  - `value-match`
  - Returns lines that match
  - ```{code-block} yaml
    :emphasize-lines: 6-7
    get-data:
      - query:
          type: html-table-row
          column-num: 2
      - query:
          type: value-match
          line-regex: "(?i)confidentiality|integrity|availability"
    ```
  - Given a value from a previous query as input, the `value-match` type will split the value into lines, and run the regex over each line, outputting the entire line if the regex matches.
* - Value
  - `value-replace`
  - Returns a replacement value on match
  - ```{code-block} yaml
    :emphasize-lines: 6-8
    get-data:
      - query:
          type: html-table-row
          column-num: 2
      - query:
          type: value-replace
          match: "SSL"
          replacement: "TLS"
    ```
  - Given a value from a previous query as input, the `value-replace` type will check if the value is an exact match for the `match:` value and if so it will return the `replacement:` value.  If there is no match, the original string is returned.
* - Value
  - `value-urldecode`
  - Returns a URL decoded version of the value
  - ```{code-block} yaml
    :emphasize-lines: 6
    get-data:
      - query:
          type: html-table-row
          column-num: 2
      - query:
          type: value-urldecode
    ```
  - Given a value from a previous query as input, the `value-urldecode` will return the URL decoded value.
  :::

### Post processing options

The `output-data:` / `post-processor:` supports the following values:

:::{list-table}
:widths: auto 
:header-rows: 1

* - Post Processor
  - Use Case
  - Example
  - Description
* - `remove-empty-rows`
  - Removes empty rows from a table
  - ```{code-block} yaml
    :emphasize-lines: 3-5
    output-data:
      post-processor:
        remove-empty-rows:
          ignore-keys: 
            - category
    ```
  - Given the output of `map-data:` (a list), remove any list rows where all the entries are empty.  Optionally specify a list of `ignore-keys:`, which are the column values in the row to ignore when checking if empty e.g. if `ignore-keys:` lists the `category` column (really `key:` name from `map-data:`) then even if it has a value, but the rest of the row is empty, that row will be removed.
* - `remove-header-row`
  - Removes the 1st row from a table
  - ```{code-block} yaml
    :emphasize-lines: 3
    output-data:
      post-processor:
        remove-header-row:
    ```
  - Given the output of `map-data:` (a list), remove the first row.  
* - `inherit-row-above-if-empty`
  - Allows a row to inherit the value of the row above in a given column
  - ```{code-block} yaml
    :emphasize-lines: 3-4
    output-data:
      post-processor:
        inherit-row-above-if-empty:
          key: category
    ```
  - Given the output of `map-data:` (a list), loop though all rows and if the value of column (really `key:` name from `map-data:`) specified by `key:` is empty, then populate it with the value from the row above.  This allows for the lazy population of tables as it avoids having to repeat the same column value many times in different rows.
* - `value-replace`
  - Returns a replacement value on match
  - ```{code-block} yaml
    :emphasize-lines: 3-9
    output-data:
      post-processor:
        value-replace:
          - match: "C"
            replacement: "Confidentiality"
          - match: "I"
            replacement: "Integrity"
          - match: "A"
            replacement: "Availability"
    ```
  - Given some input (a string), looks for any of the list of `match` values and if found outputs the corresponding `replacement` value.  If there is no match, the original string is returned.
:::