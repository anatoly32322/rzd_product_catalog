def reduce_category_tree(category_tree: dict) -> dict:
    new_category_tree = {}
    for child in category_tree.get('children', []):
        new_category_tree[child['name']] = reduce_category_tree(child)
    return new_category_tree


if __name__ == '__main__':
    import json

    with (
        open('yandex_category_tree.json') as r_file,
        open('reduced_yandex_category_tree.json', 'w') as w_file
    ):
        category_tree = json.load(r_file)['result']
        reduced_category_tree = reduce_category_tree(category_tree)
        json.dump(reduced_category_tree, w_file, indent=2, ensure_ascii=False)
