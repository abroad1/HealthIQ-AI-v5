import os
import yaml

# Resolve the path to the YAML file
yaml_path = os.path.join(os.path.dirname(__file__), "biomarker_alias_registry.yaml")

# Load the YAML contents
with open(yaml_path, "r") as f:
    ALIAS_TO_CANONICAL = yaml.safe_load(f)
