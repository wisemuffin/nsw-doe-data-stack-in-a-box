import json

# parse any version of manifest.json
from dbt_artifacts_parser.parser import parse_manifest

# with open("path/to/manifest.json", "r") as fp:
#     manifest_dict = json.load(fp)
#     manifest_obj = parse_manifest(manifest=manifest_dict)

# # parse manifest.json v1
# from dbt_artifacts_parser.parser import parse_manifest_v1

# with open("path/to/manifest.json", "r") as fp:
#     manifest_dict = json.load(fp)
#     manifest_obj = parse_manifest_v1(manifest=manifest_dict)

# # parse manifest.json v2
# from dbt_artifacts_parser.parser import parse_manifest_v2

# with open("path/to/manifest.json", "r") as fp:
#     manifest_dict = json.load(fp)
#     manifest_obj = parse_manifest_v2(manifest=manifest_dict)

# # parse manifest.json v3
# from dbt_artifacts_parser.parser import parse_manifest_v3

# with open("path/to/manifest.json", "r") as fp:
#     manifest_dict = json.load(fp)
#     manifest_obj = parse_manifest_v3(manifest=manifest_dict)

# # parse manifest.json v4
# from dbt_artifacts_parser.parser import parse_manifest_v4

# with open("path/to/manifest.json", "r") as fp:
#     manifest_dict = json.load(fp)
#     manifest_obj = parse_manifest_v4(manifest=manifest_dict)

# # parse manifest.json v5
# from dbt_artifacts_parser.parser import parse_manifest_v5

# with open("path/to/manifest.json", "r") as fp:
#     manifest_dict = json.load(fp)
#     manifest_obj = parse_manifest_v5(manifest=manifest_dict)

# # parse manifest.json v6
# from dbt_artifacts_parser.parser import parse_manifest_v6

# with open("path/to/manifest.json", "r") as fp:
#     manifest_dict = json.load(fp)
#     manifest_obj = parse_manifest_v6(manifest=manifest_dict)

# # parse manifest.json v7
# from dbt_artifacts_parser.parser import parse_manifest_v7

# with open("path/to/manifest.json", "r") as fp:
#     manifest_dict = json.load(fp)
#     manifest_obj = parse_manifest_v7(manifest=manifest_dict)

# # parse manifest.json v8
# from dbt_artifacts_parser.parser import parse_manifest_v8

# with open("path/to/manifest.json", "r") as fp:
#     manifest_dict = json.load(fp)
#     manifest_obj = parse_manifest_v8(manifest=manifest_dict)

# # parse manifest.json v9
# from dbt_artifacts_parser.parser import parse_manifest_v9

# with open("path/to/manifest.json", "r") as fp:
#     manifest_dict = json.load(fp)
#     manifest_obj = parse_manifest_v9(manifest=manifest_dict)

# # parse manifest.json v10
# from dbt_artifacts_parser.parser import parse_manifest_v10

# with open("path/to/manifest.json", "r") as fp:
#     manifest_dict = json.load(fp)
#     manifest_obj = parse_manifest_v10(manifest=manifest_dict)

# parse manifest.json v11
from dbt_artifacts_parser.parser import parse_manifest_v11

with open("./transformation/transformation_nsw_doe/target/manifest.json", "r") as fp:
    manifest_dict = json.load(fp)
    manifest_obj = parse_manifest_v11(manifest=manifest_dict)
    print(manifest_obj)