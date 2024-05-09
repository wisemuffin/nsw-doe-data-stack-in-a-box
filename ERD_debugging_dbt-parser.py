import json

from dbt_artifacts_parser.parser import parse_manifest_v11

with open("./transformation/transformation_nsw_doe/target/manifest.json", "r") as fp:
    manifest_dict = json.load(fp)
    manifest_obj = parse_manifest_v11(manifest=manifest_dict)
    print(manifest_obj)
