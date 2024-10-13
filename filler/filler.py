from copy import copy


category_tree_extension = {
    'Металлические изделия': {
        '_attributes': [],
        'Трубы': {
            '_attributes': ['Материал', 'Диаметр'],
        },
        'Рельсы': {
            '_attributes': ['Колея', 'Транспорт'],
            'Накладки': {}
        }
    },
    'Полезные ископаемые': {
        '_attributes': [],
        'Уголь': {
            '_attributes': ['Марка']
        },
        'Руды металлические': {
            '_attributes': ['Тип металла'],
        },
        'Нефть и газ природный': {
            '_attributes': [],
        },
    },
}
extension: dict


def extend_categories_and_attributes(categories_and_attributes: dict, extension: dict) -> dict:
    new_categories_and_attributes = copy(categories_and_attributes)
    for category, value in extension.items():
        if category == '_attributes':
            new_categories_and_attributes.setdefault('_attributes', []).extend(value)
            continue

        if category not in new_categories_and_attributes:
            new_categories_and_attributes[category] = {}

        new_categories_and_attributes[category] = extend_categories_and_attributes(
            categories_and_attributes=new_categories_and_attributes[category],
            extension=value,
        )

    return new_categories_and_attributes


if __name__ == '__main__':
    import json

    with (
        open('reduced_yandex_category_tree.json') as r_file,
        open('output1.json', 'r') as r_file1,
        open('extended_yandex_category_tree.json', 'w') as w_file
    ):
        tree = json.load(r_file)
        extension = json.load(r_file1)
        extended_tree = extend_categories_and_attributes(tree, category_tree_extension)
        json.dump(extended_tree, w_file, indent=2, ensure_ascii=False)
