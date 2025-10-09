def left_leaf(root: int) -> int:
    """Вычисляет значение левого листового узла.

    Args:
        root: целое число

    Returns:
        квадрат целого числа
    """
    return root ** 2


def right_leaf(root: int) -> int:
    """Вычисляет значение правого листового узла.

    Args:
        целое число

    Returns:
        квадрат целого числа увеличенный на 2
    """
    return 2 + root ** 2


def gen_bin_tree(height: int, root: int, l_l=left_leaf, l_r=right_leaf):
    """Генерирует бинарное дерево в виде словарей.

    Строит дерево с помощью рекурсии, каждый узел которой - словарь

    Args:
        height: Высота дерева
        root: целое число
        l_l: Функция для вычисления левых веток
        l_r: Функция для вычисления правых веток

    Returns:
        Словарь, где ключами являются значения root, а значениями - список результатов работы функции

    """
    if height <= 1:
        return {str(root): []}
    return {str(root): [gen_bin_tree(height - 1, l_l(root), l_l, l_r),
                        gen_bin_tree(height - 1, l_r(root), l_l, l_r)]}


def main():
    """Генерирует и выводит бинарное дерево"""
    print(gen_bin_tree(3, 11))


if __name__ == '__main__':
    main()