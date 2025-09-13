def SumTwo(num, target):
    rez = []
    if len(num) > 0 and isinstance(num,
                                   list):  # проверяем является ли num списком, а так же проверяем чтобы был не пустым
        for i in range(len(num) - 1):  # начинаем перебор значений
            for j in range(i + 1, len(num)):
                if isinstance(num[i], int) and isinstance(num[j],
                                                          int):  # проверка являются ли оба значения числами, если да - считаем, иначе говорим Nont
                    if num[i] + num[j] == target:
                        if i not in rez:
                            rez += [i]
                        if j not in rez:
                            rez += [j]
                else:
                    return "None"
        if len(rez) > 0:  # проверяем есть ли ответы, если да - берем первые два т.к. все элементы добавлялись попарно соответственно пара с минимальным индексом будет первая
            return rez[0:2]
        else:
            return 'None'
    else:
        return 'None'


num = [3]
print(SumTwo(num, 1))
