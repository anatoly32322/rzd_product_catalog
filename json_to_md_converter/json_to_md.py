import json
import os
import sys


def dfs(node: any, depth: int, fout):
    if not isinstance(node, dict) and not isinstance(node, list):
        fout.write(f"{'#' * depth} {node}\n")
        return
    elif isinstance(node, dict):
        for nested_node_key, nested_node_value in node.items():
            if nested_node_key == "status" or nested_node_key == "recommendationTypes":
                continue
            if not isinstance(nested_node_value, dict) and not isinstance(nested_node_value, list):
                if nested_node_key == "name":
                    dfs(nested_node_value, depth + 1, fout)
                continue
            if isinstance(nested_node_value, list):
                if nested_node_key != "children":
                    fout.write(f"{'#' * depth} {nested_node_key}\n")
                dfs(nested_node_value, depth, fout)
                continue
            fout.write(f"{'#' * depth} {nested_node_key}\n")
            dfs(nested_node_value, depth + 1, fout)
    elif isinstance(node, list):
        for nested_node in node:
            dfs(nested_node, depth + 1, fout)


def convert(data: dict):
    with open("output.md", "w+") as fout:
        dfs(data, 0, fout)


def run(args: list):
    filepath = args[1]
    if not os.path.exists(filepath):
        print("Wrong filepath")
        return
    with open(filepath, "r") as fin:
        content = json.loads(fin.read())
        convert(content)


if __name__ == "__main__":
    run(sys.argv)
