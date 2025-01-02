import random


class OrderedSet:

    # Конструктор для создания упорядоченного множества из size элементов.
    # По умолчанию отношение порядка не задано (все элементы несравнимы).
    def __init__(self, size: int):
        # Установим размер матрицы.
        self.size = size
        if size > 10:
            print("Внимание: матрица такого размера будет плохо выводиться")
        # Создадим матрицу нужного размера, заполненную нулями.
        self.matrix = [[0 for _ in range(size)] for _ in range(size)]
        # Наше упорядоченное множество (У. М.) будем представлять матрицей:
        # если x > y, то matrix[x][y] = 1.
        # Другие случаи (x < y, x и y несравнимы) явно не кодируются, подразумевается, что matrix[x][y] = 0.

    # Основной метод для установки отношения порядка в У. М. После вызова этого метода x становится > y.
    # Замечание: в метод встроено свойство транзитивности, следовательно, если
    # x > y и y > z, то 1. не нужно устанавливать x > z (это будет сделано автоматически). 2. Установка z > x приведет к ошибке.
    def set_greater(self, x: int, y: int) -> None:
        # Проверим возможность установки отношения x > y (отсутствие противоречий с уже установленными отношениями).
        for i in range(self.size):
            if (self.matrix[y][i] == 1 or y == i) and (self.matrix[i][x] == 1 or x == i):
                # Если найдется i, такое что y >= i и i >= x, причем x != y,
                raise ValueError("Предлагаемое отношение порядка противоречит аксиоматике")
                # то возникает противоречие, так как из y >= i и i >= x следует y >= x, что противоречит желаемому x > y.

        # Противоречий нет, устанавливаем отношение порядка x > y.
        self.matrix[x][y] = 1
        # Реализуем свойство транзитивности:
        for i in range(self.size):
            if self.matrix[y][i] == 1:
                # Если y > i (и уже установлено x > y),
                self.matrix[x][i] = 1
                # то x > i (транзитивность).

            if self.matrix[i][x] == 1:
                # Если i > x (и уже установлено x > y),
                self.matrix[i][y] = 1
                # то i > y (транзитивность).

    # Метод для вывода матрицы смежности в консоль.
    def __str__(self):
        res = ""
        res += "  "
        for i in range(self.size):
            res += str(i) + " "
        res += "\n"
        res += "  " + "-" * (self.size * 2 - 1) + "\n"
        i = 0
        for comb in self.matrix:
            res += str(i) + "|"
            i += 1
            for elem in comb:
                res += str(elem)
                res += " "

            res += '\n'
        return res

    # Вспомогательный алгоритм сортировки цепи (используется быстрая сортировка).
    def sort_chain(self, nums) -> list:
        if not self.is_chain(nums):
            # Если nums не является цепью, сортировка невозможна.
            raise ValueError("Не цепь")

        if len(nums) <= 1:
            return nums
            # Базовый случай рекурсии.
        else:
            # Случайно выберем опорный элемент (pivot).
            q = random.choice(nums)
            s_nums = []
            m_nums = []
            e_nums = []
            for n in nums:
                if self.matrix[q][n]:
                    # Элементы, которые меньше опорного.
                    s_nums.append(n)
                elif self.matrix[n][q]:
                    # Элементы, которые больше опорного.
                    m_nums.append(n)
                else:
                    # Элементы, равные опорному (хотя равенство в У.М. явно не поддерживается).
                    e_nums.append(n)
            # Рекурсивно вызываем сортировку для меньших и больших элементов.
            return self.sort_chain(s_nums) + e_nums + self.sort_chain(m_nums)

    # Вспомогательный метод проверки, является ли последовательность цепью.
    def is_chain(self, chain):
        return all([self.is_comparable(x, y) or x == y for x in chain for y in chain])


    # Вспомогательный метод проверки, является ли последовательность антицепью.
    def is_anti_chain(self, chain):
        return all([not self.is_comparable(x, y) or x == y for x in chain for y in chain])

    # Проверка на сравнимость двух элементов.
    def is_comparable(self, x, y):
        return self.matrix[x][y] or self.matrix[y][x]

    # Наивный алгоритм дополнения цепи до максимальной (полный перебор).
    def complete_chain_naive(self, chain: list):
        if not self.is_chain(chain):
            raise ValueError("Не цепь")
        # Найдем элементы, не входящие в цепь.
        remainder = [x for x in range(self.size)]
        for elem in chain:
            remainder.remove(elem)

        for x in remainder:
            b = all([self.is_comparable(x, y) for y in chain])
            # Если элемент x сравним со всеми элементами цепи,
            # то его можно добавить к цепи.
            if b:
                chain.append(x)
        return chain

    # Улучшенный метод нахождения максимальной цепи (перебор с сохранением внутреннего порядка).
    def complete_chain(self, chain: list):
        if not self.is_chain(chain):
            raise ValueError("Не цепь")
        # Найдем элементы, не входящие в цепь.
        remainder = [x for x in range(self.size)]
        for elem in chain:
            remainder.remove(elem)

        # Отсортируем исходную цепь.
        chain = self.sort_chain(chain)

        # Итерируем по всем элементам дополнения.
        for x in remainder:
            f = 1
            for i in range(len(chain)):
                y = chain[i]
                if not self.is_comparable(x, y):
                    f = 0
                    break
                if self.matrix[y][x]:
                    # Если y > x, то мы нашли место в цепи для вставки x.
                    chain.insert(i, x)
                    f = 0
                    break
            if f:
                # Если не найдено место для вставки в середину, но элемент сравним со всеми,
                # значит, он больше всех элементов цепи и добавляется в конец.
                chain.append(x)

        return chain

    # Алгоритм дополнения антицепи до максимальной (перебор).
    def complete_anti_chain(self, chain):
        if not self.is_anti_chain(chain):
            raise ValueError("Не антицепь")
        # Найдем элементы, не входящие в антицепь.
        remainder = [x for x in range(self.size)]
        for elem in chain:
            remainder.remove(elem)

        for x in remainder:
            b = all([not self.is_comparable(x, y) for y in chain])
            # Если элемент x не сравним со всеми элементами антицепи,
            # то его можно добавить к антицепи.
            if b:
                chain.append(x)
        return chain

    # Метод для нахождения длины (максимальной цепи) множества.
    def find_len(self):
        s = [x for x in range(self.size)]
        res = 0
        cur = [0]
        while len(s) != 0:
            cur = self.complete_chain(cur)
            res = max(res, len(cur))
            for elem in cur:
                if elem in s:
                    s.remove(elem)
            if len(s) == 0:
                break
            cur = [s[0]]

        return res-1

    # Метод для нахождения ширины (максимальной антицепи) множества.
    def find_width(self):
        s = [x for x in range(self.size)]
        res = 0
        cur = [0]
        while len(s) != 0:
            cur = self.complete_anti_chain(cur)
            res = max(res, len(cur))
            for elem in cur:
                if elem in s:
                    s.remove(elem)
            if len(s) == 0:
                break
            cur = [s[0]]

        return res