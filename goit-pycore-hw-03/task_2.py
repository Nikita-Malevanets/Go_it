import random


def get_numbers_ticket(min: int, max: int, quantity: int) -> list[int]:
    """
        Returns a sorted list of unique random numbers within the given range.
        If parameters are invalid, returns an empty list.
    """
    if min < 1 or max > 1000 or quantity > (max - min + 1) or (min > max):
        return []
    generator_numbers = random.sample(range(min, max + 1), quantity)
    return sorted(generator_numbers)


lottery_numbers = get_numbers_ticket(1, 49, 6)
print("Ваші лотерейні числа:", lottery_numbers)
