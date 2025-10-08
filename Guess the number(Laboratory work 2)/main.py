def guess_number(find_nom: int, numbers: list[int], way: str) -> tuple[int, int | None]:
    """
        Ищет число в массиве указанным способом и возвращает результат поиска.

        Args:
            find_nom (int): Число, которое необходимо найти
            numbers (list[int]): Массив чисел для поиска
            way (str): Способ поиска ('seq' - линейный, 'bin' - бинарный)

        Returns:
            tuple[int, int | None]: Кортеж содержащий:
                - Найденное число (или исходное, если не найдено)
                - Количество шагов поиска или None если число не найдено
    """
    if find_nom not in numbers or len(numbers) == 0:
        return find_nom, None
    if way == 'seq':
        count = 0
        for i in numbers:
            count += 1
            if i == find_nom:
                return i, count
    elif way == 'bin':

        numbers.sort()
        left = 0
        right = len(numbers)
        count = 0
        while right > left:
            count += 1
            mid = (left + right) // 2
            if numbers[mid] == find_nom:
                return numbers[mid], count
            elif numbers[mid] < find_nom:
                left = mid + 1
            else:
                right = mid
    else:
        return find_nom, None


def main():
    """
       Основная функция для взаимодействия с пользователем.

       Запрашивает у пользователя параметры поиска и возвращает результат.

       Returns:
           tuple[int, int | None]: Результат выполнения функции guess_number
    """
    find_nome = int(input("Введите число "))
    s = input("Хотите вы сами вводить массив? Yes/No ")
    numbers = []
    if s == 'Yes':
        s = input('Введите значения массива через пробел ')
        s = s.split()
        for i in s:
            numbers += [int(i)]
    if s == 'No':
        a, b = map(int, input("Через пробел введите интервал значений ").split())
        for i in range(a, b + 1):
            numbers += [i]
    way = input("Каким способом вы хотите найти число? bin/seq ")
    return guess_number(find_nome, numbers, way)

# print(main())
