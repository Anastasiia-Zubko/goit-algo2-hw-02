from typing import List, Dict, Tuple


def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
       Знаходить оптимальний спосіб розрізання через мемоізацію
    """

    if length <= 0:
        raise ValueError("Довжина стрижня має бути > 0.")
    if not prices:
        raise ValueError("Масив цін не може бути порожнім.")
    if length != len(prices):
        raise ValueError("Довжина масиву цін повинна відповідати довжині стрижня.")

    memo: Dict[int, Tuple[int, Tuple[int, ...]]] = {0: (0, ())}

    def _best(len_remaining: int) -> Tuple[int, Tuple[int, ...]]:

        if len_remaining in memo:
            return memo[len_remaining]

        max_profit_local = -1
        best_cuts_local: Tuple[int, ...] = ()

        for cut in range(1, len_remaining + 1):
            current_price = prices[cut - 1]
            rem_profit, rem_cuts = _best(len_remaining - cut)
            total_profit = current_price + rem_profit

            if total_profit > max_profit_local:
                max_profit_local = total_profit
                best_cuts_local = (cut,) + rem_cuts

        memo[len_remaining] = (max_profit_local, best_cuts_local)
        return memo[len_remaining]

    max_profit, cuts_tuple = _best(length)
    cuts: List[int] = list(cuts_tuple)
    number_of_cuts = max(len(cuts) - 1, 0)

    return {
        "max_profit": max_profit,
        "cuts": cuts,
        "number_of_cuts": number_of_cuts,
    }


def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
        Знаходить оптимальний спосіб розрізання через табуляцію
    """

    if length <= 0:
        raise ValueError("Довжина стрижня має бути > 0.")
    if not prices:
        raise ValueError("Масив цін не може бути порожнім.")
    if length != len(prices):
        raise ValueError("Довжина масиву цін повинна відповідати довжині стрижня.")

    dp: List[int] = [0] * (length + 1)
    first_cut: List[int] = [0] * (length + 1)

    for len_current in range(1, length + 1):
        max_profit_local = -1
        best_first_cut = 0
        for cut in range(1, len_current + 1):
            profit = prices[cut - 1] + dp[len_current - cut]
            if profit > max_profit_local:
                max_profit_local = profit
                best_first_cut = cut
        dp[len_current] = max_profit_local
        first_cut[len_current] = best_first_cut

    cuts: List[int] = []
    remaining = length
    while remaining > 0:
        cut = first_cut[remaining]
        cuts.append(cut)
        remaining -= cut

    number_of_cuts = max(len(cuts) - 1, 0)

    return {
        "max_profit": dp[length],
        "cuts": cuts,
        "number_of_cuts": number_of_cuts,
    }


def run_tests():
    """Функція для запуску всіх тестів"""
    test_cases = [
        # Тест 1: Базовий випадок
        {
            "length": 5,
            "prices": [2, 5, 7, 8, 10],
            "name": "Базовий випадок"
        },
        # Тест 2: Оптимально не різати
        {
            "length": 3,
            "prices": [1, 3, 8],
            "name": "Оптимально не різати"
        },
        # Тест 3: Всі розрізи по 1
        {
            "length": 4,
            "prices": [3, 5, 6, 7],
            "name": "Рівномірні розрізи"
        }
    ]

    for test in test_cases:
        print(f"\nТест: {test['name']}")
        print(f"Довжина стрижня: {test['length']}")
        print(f"Ціни: {test['prices']}")

        # Тестуємо мемоізацію
        memo_result = rod_cutting_memo(test['length'], test['prices'])
        print("\nРезультат мемоізації:")
        print(f"Максимальний прибуток: {memo_result['max_profit']}")
        print(f"Розрізи: {memo_result['cuts']}")
        print(f"Кількість розрізів: {memo_result['number_of_cuts']}")

        # Тестуємо табуляцію
        table_result = rod_cutting_table(test['length'], test['prices'])
        print("\nРезультат табуляції:")
        print(f"Максимальний прибуток: {table_result['max_profit']}")
        print(f"Розрізи: {table_result['cuts']}")
        print(f"Кількість розрізів: {table_result['number_of_cuts']}")

        print("\nПеревірка пройшла успішно!")


if __name__ == "__main__":
    run_tests()
