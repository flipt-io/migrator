import os
import questionary
import argparse
from source import launchdarkly
from exporter import export_to_yaml


def main():
    sources = ["LaunchDarkly"]  # "Split", "Unleash", "Flagsmith"]
    parser = argparse.ArgumentParser(
        description="Migrate from a feature flag source to Flipt."
    )
    parser.add_argument(
        "--source",
        type=str,
        choices=sources,
        help="The source to migrate from.",
    )
    parser.add_argument(
        "--out",
        type=str,
        help="The location to export Flipt data.",
    )
    args = parser.parse_args()

    if args.out is not None:
        path = args.out
    else:
        path = questionary.path(
            "Location to export Flipt data:", ".", only_directories=True
        ).ask()

    transformer = None

    if args.source is not None:
        competitor = args.source
    else:
        competitor = questionary.select(
            "Source:",
            choices=sources,
        ).ask()

    if competitor == "LaunchDarkly":
        api_key = os.getenv("LAUNCHDARKLY_API_KEY")
        if not api_key:
            api_key = questionary.password("LaunchDarkly API Key:").ask() or ""

        project_key = os.getenv("LAUNCHDARKLY_PROJECT_KEY")
        if not project_key:
            project_key = questionary.text("LaunchDarkly Project Key:", "default").ask()

        transformer = launchdarkly.Transformer(api_key, project_key)
    else:
        print("Unsupported source.")
        return

    data = transformer.transform()
    if not data:
        print("No data to export.")
        return

    export_to_yaml(data, path)
    print("✅ Migration completed successfully.")


if __name__ == "__main__":
    main()
