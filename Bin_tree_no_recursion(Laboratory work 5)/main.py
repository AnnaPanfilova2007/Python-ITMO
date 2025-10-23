from queue import Queue


def bin_tree_No_recursion(height: int, root: int, l_b=lambda x: x ** 2, r_b=lambda x: x ** 2 + 2):
    """
    Генерирует бинарное дерево с использованием итеративного подхода.

    Args:
        height (int): Высота генерируемого бинарного дерева
        root (int): Значение корневого узла дерева
        l_b (callable, optional): Функция для вычисления левого потомка.
                                 По умолчанию x**2.
        r_b (callable, optional): Функция для вычисления правого потомка.
                                 По умолчанию x**2 + 2.

    Returns:
        dict: Словарь, представляющий бинарное дерево в формате:
              {root_value: [left_subtree, right_subtree]}
    """
    arr = [[{str(root): []}, root]]
    if height < 1:
        return {str(root): []}
    height += 1
    bin_di = {}
    k = 0
    while height != 1:
        old_le = len(arr)
        for i in range(k, len(arr)):
            s = str(arr[i][1])
            arr += [[{str(l_b(arr[i][1])): []}, l_b(arr[i][1])]]
            arr.append([{str(r_b(arr[i][1])): []}, r_b(arr[i][1])])

        height -= 1
        k = old_le
    for i in range(len(arr) // 2):
        arr[i][0][str(arr[i][1])].append(arr[i * 2 + 1][0])
        arr[i][0][str(arr[i][1])].append(arr[i * 2 + 2][0])
    return arr[0][0]


def bin_tree_bfs(height: int, root: int, l_b=lambda x: x ** 2, r_b=lambda x: x ** 2 + 2):
    """
    Создает бинарное дерево заданной высоты, используя алгоритм поиска в ширину.
    Узлы обрабатываются уровень за уровнем с помощью очереди.

    Args:
        height (int): Высота генерируемого бинарного дерева
        root (int): Значение корневого узла дерева
        l_b (callable, optional): Функция для вычисления левого потомка.
                                 По умолчанию x**2.
        r_b (callable, optional): Функция для вычисления правого потомка.
                                 По умолчанию x**2 + 2.

    Returns:
        dict: Словарь, представляющий бинарное дерево в формате:
              {root_value: [left_subtree, right_subtree]}
    """
    queue = Queue()
    di = {str(root): []}
    queue.put(di)
    for i in range(2 ** height - 1):
        current = queue.get()
        for key in current:
            l_di = {str(l_b(int(key))): []}
            r_di = {str(r_b(int(key))): []}
            current[key] += [l_di, r_di]
            queue.put(l_di)
            queue.put(r_di)
    return di


def main():
    """Генерирует и выводит бинарное дерево."""
    print(bin_tree_No_recursion(3, 1, lambda x: x + 1, lambda x: x + 2))
    print(bin_tree_bfs(3, 1, lambda x: x + 1, lambda x: x + 2))


if __name__ == '__main__':
    main()
