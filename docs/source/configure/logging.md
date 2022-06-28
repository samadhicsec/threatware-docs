# Logging

threatware is very configurable which unfortunately means there are a lot of things that can go wrong.  While (hopefully) there are many meaningful error messages, sometimes the error message is simply to 'look at the logs'.

threatware supports the standard python log levels:

- `ERROR` - something has happened that should not have happened
- `WARNING` - something unexpected happened and it might affect the result
- `INFO` - these things happened
- `DEBUG` - everything that happened

By default the log level is `WARNING` and the logs are printed to stderr (in the lambda environment they are accessible via Cloudwatch).

The log level can be set, in both the lambda and CLI environments, by setting an environment variable called `THREATWARE_LOG_LEVEL` to one of the above values (case sensitive).

:::{tip}
If in the CLI environment don't forget you need to `export` the environment variable for it to be picked up by threatware e.g.

`export THREATWARE_LOG_LEVEL=INFO`
:::

The `INFO` and `DEBUG` log levels are useful for advanced users trying to debug actions like `convert` and `verify` if the output of threatware is not what is expected.  The `INFO` level is also useful if configuration errors are encountered and no meaningful error message was returned.