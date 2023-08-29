# Flipt Migrator

This is a tool to migrate feature flags from one source (e.g. competitor) to Flipt.

It works by exporting the feature flags from the source into a set of `*.features.yml` files that can then be imported into Flipt or run as the source data with Flipt in ['local' mode](https://www.flipt.io/docs/configuration/storage#local)

## Usage

```shell
usage: flipt-migrate [-h] [--source {LaunchDarkly}] [--out OUT]

Migrate from a feature flag source to Flipt.

options:
  -h, --help            show this help message and exit
  --source {LaunchDarkly}
                        The source to migrate from.
  --out OUT             The location to export Flipt data. Defaults to current directory.
```

## Sources

### LaunchDarkly

To export feature flags from LaunchDarkly, you will need to set the following environment variables or you will be prompted for them:

- `LAUNCHDARKLY_API_KEY` - Your LaunchDarkly API key
- `LAUNCHDARKLY_PROJECT_KEY` - The LaunchDarkly project key to export (optional)
