# Authentication

Any usage of threatware requires authentication to be configured.

In order to read threat model documents threatware needs to be able to authenticate to (depending on where you store your documents, at least one of):
- Confluence
- Google Docs

In order for the management functionality of threatware to store and retrieve threat model metadata and models, threatware needs to be able to authenticate to:
- Git repository (using SSH keys)

Configuring authentication differs by whether you are using threatware CLI or as a lambda.

:::{admonition} Note
All the relative paths mentioned below are relative the threatware configuration directory, as detailed in [](./configuration.md)
:::

## Authentication for threatware CLI

### Confluence

By default the credentials used to authenticate to Confluence should be stored in a `.atlassian` file.  This is configurable in `providers/providers_config.yaml` via `providers:cli:confluence_creds_file` key.

For Confluence the URL of the Confluence server is not stored in threatware configuration files, but rather with the credentials used to authenticate to Confluence.

The format of the file depends on the type of Confluence server you need to authenticate to.

#### Cloud Confluence

The format is:

:::ini
[DEFAULT]
url = <your Confluence URL>
username = <your Confluence username>
api_token = <your Confluence API Token>
cloud = True
:::

This is also the default, meaning that if the `cloud` field is not present, it is assumed to be `True`

#### Server Confluence with PAT

The format is:

:::ini
[DEFAULT]
url = <your Confluence URL>
token = <your Confluence Personal Access Token>
cloud = False
:::

#### Server Confluence with Username and Password

The format is:

:::ini
[DEFAULT]
url = <your Confluence URL>
username = <your Confluence username>
password = <your Confluence password>
cloud = False
:::

It is not recommended that you connect with your Confluence username and password, it is better security practice to use a PAT.

### Google Docs

Google uses OAuth2.0 to authorise access to its APIs, and OAuth2.0 requires a Client ID in order to be used, and a Client ID requires registering an OAuth2.0 application with Google.  You have to register your own application because threatware cannot be published with this information because it contains a Client Secret.

Follow these [instructions](https://developers.google.com/identity/protocols/oauth2/native-app) for how to register an application.
- If you haven't used the gcloud console before you may need to first (create a Project)[https://cloud.google.com/resource-manager/docs/creating-managing-projects#creating_a_project]
- The API you need to enable is `Google Drive API`
- When you select `+Create Credentials` -> `OAuth client ID` choose the Application Type as `Desktop App`
- Download the credentials JSON file for the application, and save it to `convertors/gdoc_convertor/credentials.json` (this can be customised in `providers/providers_config.yaml` via `providers:cli:google:credentials_file` key).

When threatware attempts to access the Google Doc threat model for the first time a browser window will open and you will be asked to authorise access.  If successful, this stores a `token.json` file on the file system, and this is used for future requests (so authorisation using the browser window is a one-off experience).

Note, for Google Docs, passing in the document ID is sufficient to know the location of the document as all documents share the same URL.

### Git Repository

Authentication to the git repository uses the SSH keys of the current user, usually stored in `~/.ssh`.

The location of the git repository is specified in `manage/manage_config.yaml` via

:::yaml
manage-config:
    storage:
        gitrepo:
            remote: <git location e.g. git@github.com:username/project>
:::

The `remote` value to specify is passed directly to the `git` command and so it's many variations are supported e.g. specifying a specific key via `~/.ssh/config`.

## Authentication for threatware AWS lambda

By default ALL the credentials used to authenticate should be stored in AWS Secrets Manager, in a secret called `threatware` in `eu-west-2`.  

The secret name/region is configurable in `providers/providers_config.yaml` via `providers:aws.lambda:secret_name` and `providers:aws.lambda:region` keys.

### Confluence

For Confluence the credentials must be stored in a Secret Key called `confluence` and a Secret Value as a JSON blob (under the Secret Name `threatware`).

For Confluence the URL of the Confluence server is not stored in threatware configuration files, but rather with the credentials used to authenticate to Confluence.

The format of the JSON value depends on the type of Confluence server you need to authenticate to.

#### Cloud Confluence

The format is:

:::json
{ 
    "url": "<your Confluence URL>", 
    "username": "<your Confluence username>",
    "api_token": "<your Confluence API Token>",
    "cloud": "True"
}
:::

This is also the default, meaning that if the `cloud` field is not present, it is assumed to be `True`

#### Server Confluence with PAT

The format is:

:::json
{ 
    "url": "<your Confluence URL>", 
    "token": "<your Confluence Personal Access Token>",
    "cloud": "False"
}
:::

#### Server Confluence with Username and Password

The format is:

:::json
{ 
    "url": "<your Confluence URL>", 
    "username": "<your Confluence username>",
    "password": "your Confluence password",
    "cloud": "False"
}
:::

It is not recommended that you connect with your Confluence username and password, it is better security practice to use a PAT.

### Google Docs

Google uses OAuth2.0 to authorise access to its APIs, and OAuth2.0 requires a Client ID in order to be used, and a Client ID requires registering a service account (when a user cannot explicitly authorise an application, as is the case with using a lambda).

Follow these [instructions](https://developers.google.com/identity/protocols/oauth2/service-account) for how to register a service account.
- If you haven't used the gcloud console before you may need to first (create a Project)[https://cloud.google.com/resource-manager/docs/creating-managing-projects#creating_a_project]
- The API you need to enable is `Google Drive API`
- To generate credentials select `+Create Credentials` -> `Service Account` and populate the required information.
    - Note, make a note of the Service Account email address.  *You will need to Share the Google Doc with this email address in order for the Service Account to have access.*
- Download the JSON key file for the service account, and copy the contents to a Secret Key named `google`.  It will have the following format.

:::json
{
    "type": "service_account", 
    "project_id": "<project-id>", 
    "private_key_id": "<private-key-id>", 
    "private_key": "-----BEGIN PRIVATE KEY-----\nABC...DEF\nGHI...JKL\n...\n-----END PRIVATE KEY-----\n", 
    "client_email": "<client_email>", 
    "client_id": "<client_id>", 
    "auth_uri": "https://accounts.google.com/o/oauth2/auth", 
    "token_uri": "https://oauth2.googleapis.com/token", 
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs", 
    "client_x509_cert_url": "<client_x509_cert_url>" 
}
:::

### Git Repository

Authentication to the git repository uses SSH keys, which will need to be generated for threatware and added to the repository in order to allow access (for the exact method of generating the key and enabling it for the repo please consult the documentation of your git server e.g. [GitHub](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)).

After generating the SSH key you should have a public key (e.g. `~/.ssh/id_ed25519.pub`) and a private key (e.g. `~/.ssh/id_ed25519`), and the contents of these files need to be copied into a Secret Key named `git`, into respective entries.  It will have the following format:

:::json
{
    "public-key":"ssh-ed25519 ABC...DEF <service account email address>", 
    "private-key":"-----BEGIN OPENSSH PRIVATE KEY-----\nABC...DEF\nGHI..JKL\n...\n-----END OPENSSH PRIVATE KEY-----\n"
}
:::

The location of the git repository is specified in `manage/manage_config.yaml` via

:::yaml
manage-config:
    storage:
        gitrepo:
            remote: <git location e.g. git@github.com:username/project>
:::

The `remote` value to specify is passed directly to the `git` command and so it's many variations are supported e.g. specifying a specific key via `~/.ssh/config`.