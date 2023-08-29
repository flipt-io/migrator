import yaml
import os

from models.flipt import Collection
from pydantic_yaml import to_yaml_str


def export_to_yaml(data: Collection, output_path):
    for namespace, d in data.namespaces.items():
        f = os.path.join(output_path, f"{namespace}.features.yml")
        with open(f, "w") as file:
            file.write(to_yaml_str(d))
