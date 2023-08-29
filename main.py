import os
import questionary
from source import launchdarkly
from exporter import export_to_yaml

def main():
    path = questionary.path("Location to export Flipt data:", ".", only_directories=True).ask()
    transformer = None
    data = None

    competitor = questionary.select(
            "Source:",
            choices=["LaunchDarkly", "Split", "Unleash", "Flagsmith"],
        ).ask()
    
    if competitor == 'LaunchDarkly':
        api_key = os.getenv('LAUNCHDARKLY_API_KEY')
        if not api_key:
            api_key = questionary.password("LaunchDarkly API Key:?").ask() or ""

        transformer = launchdarkly.Transformer(api_key)
    else :
        print('Unsupported source.')
        return

    data = transformer.transform()
    if not data:
        print('No data to export.')
        return
    
    export_to_yaml(data, path)
    print('Migration completed successfully. ✅')

if __name__ == '__main__':
    main()
