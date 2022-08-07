# Configuration

threatware has many different configuration options.  threatware also has options for how you can specify those configuration options.

The default approach is to use *dynamic configuration*.  This allows a separate git repository to be used to store threatware configuration.  threatware will clone this configuration (if it hasn't already) when it executes.  This allows dynamic updates to the configuration by making changes to the configuration in the git repository.  Dynamic configuration can be used with either the lambda or CLI usage of threatware.

Alternatively threatware can use *static configuration*.  The configuration information for threatware is bundled with the threatware code, and the only way to change it is to redeploy the code.  Static configuration can be used with either the lambda or CLI usage of threatware.

As threatware must know which type of configuration to use, but it can't read this from configuration itself, environment variables are used:

- `THREATWARE_CONFIG_DYNAMIC=False` enables *static configuration*
- `THREATWARE_CONFIG_DYNAMIC=True` or if the environment variable is not set, this enables *dynamic configuration* (this is the default and is only not used when static configuration is specifically enabled)

## Dynamic Configuration

If dynamic configuration is being used then by default threatware will locally clone the configuration at <https://github.com/samadhicsec/threatware-config>.  Initially this is fine for CLI usage as threatware will only do this once (as if it detects existing configuration it does not overwrite it), but this isn't very useful for lambda usage.

To configure dynamic configuration for threatware we use the following environment variables:
:::{tip}
If using threatware via the CLI then you don't need to set any of these environment variables.  When first run (with an action specified) threatware will download the default configuration and you can then just edit that directly (in `~/.threatware`)
:::

- `THREATWARE_CONFIG_DIR` is the path to the directory where the git repo will be cloned.  By default this is `~/.threatware` for CLI usuage and `/tmp/.threatware` for lambda usuage.  If threatware detects this directory already exists it will assume that all the configuration is already present - it will not clone the git repo or overwrite the contents.
  :::{admonition} Warning
  :class: warning
  This directory **must not exist** already.  **Do not** create an empty directory for configuration.  As `git clone` is used, it will fail if the directory already exists.
  :::
- `THREATWARE_CONFIG_REPO` is the git repo to clone configuration from.  If this is not set the default value is `https://github.com/samadhicsec/threatware-config`.
  :::{tip}
  If the repo value you specify begins with `git@` then:
  - for CLI usage the user's git SSH credentials will be used to clone the repo
  - for lambda usage the environment variables specifying git credentials will need to be set (see below)
  
  Otherwise, threatware will attempt to anonymously clone the git repo.
  :::
- `THREATWARE_CONFIG_REPO_BRANCH` is the branch or tag to use when cloning the repo.  This allows a single configuration repo to be used that contains multiple different configurations.  The default value is the current version of threatware (this is so the correct configuration can be downloaded when the default repo is used).
- `THREATWARE_AWS_SECRET_NAME` is the name of the AWS SecretManager secret where threatware's git credentials are stored.  This variable only needs to be set when using threatware as a lambda and the git repo containing configuration requires authentication.  Ideally this value should be the same as configured for [](./authentication.md#authentication-for-threatware-aws-lambda), although it can be different, but it must have the same SecretKey name and content format.
- `THREATWARE_AWS_SECRET_REGION` is the AWS region where the `THREATWARE_AWS_SECRET_NAME` exists.

### Using a custom git configuration repository

For dynamic configuration of threatware as lambda you will need to create your own git repo containing the configuration.

The simplest method to do this is to simple fork the default repo <https://github.com/samadhicsec/threatware-config>.

If that is not an option then you can follow these instructions:

1. Create an emtpy git repository at a location of your choice
2. Clone that repo locally and cd into that repo
3. Add an additional remote to your repo

    ```shell
    git remote add upstream https://github.com/samadhicsec/threatware-config
    ```
4. Create a branch and fetch the new remote

    ```shell
    git checkout -b upstream-merge
    git fetch upstream
    git merge --allow-unrelated-histories upstream/main
    ```
5. You know have the configuration locally on a branch.  If desired you can now start to make configuration changes, for instance specifying authentication (see [](./authentication.md)).  Commit any updates to the branch.
6. When updates are complete, push to origin

    ```shell
    git push -u origin upstream-merge
    ```

You can also tag your configuration if you want, or leave your changes on a specific branch.  threatware can be configured to read a tag or branch of the repo using the `THREATWARE_CONFIG_REPO_BRANCH` environment variable.

### Configuration vs Extension

threatware supports being extended with custom code in various ways, for example by defining new verifiers.  Dynamic configuration however, cannot specify any of these extensions, and to use an extension, static configuration would be need to used, which requires a redeploy.  This helps to ensure that people given access to the configuration git repo cannot make configurations that allow them to specify arbitrary code to be executed.

## Static Configuration

Static configuration would mainly be used in situations where your configuration rarely if ever changed, or your environment demands that changes go through the full deploy process, or you have custom extensions to threatware.  It also would usually only be applicable to lambda usage.  To leverage static configuration or lambda you would need to clone the threatware repo (i.e. <https://github.com/samadhicsec/threatware>), make changes to the configuration files, and build the docker image for deployment to lambda.
