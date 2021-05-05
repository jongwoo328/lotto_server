from model import FullLotto


num_col_list = ['num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'bonus']
def get_numbers(lotto: FullLotto) -> list:
    result = []
    for col in num_col_list:
        result.append(getattr(lotto, col))
    return result

def check(set1: set, set2: set, bonus: int, prize: int) -> bool:
    common_set = set1 & set2
    if prize == 2:
        return bonus in common_set and len(common_set) == 6
    elif prize == 3:
        return len(common_set) == 5
    else:
        raise ValueError('parameter "prize" is invalid.')

def check_second_and_third(lottos: list, picked: list, q: list) -> bool:
    current_set = set(picked)
    for lotto in lottos:
        past_set = set(get_numbers(lotto))
        is_second = None
        is_third = None
        if 'except_second' in q:
            is_second = check(set1=past_set, set2=current_set, bonus=lotto.bonus, prize=2)
        if 'except_third' in q:
            is_third = check(set1=past_set, set2=current_set, bonus=lotto.bonus, prize=3)
        if is_second or is_third:
            return True
    else:
        return False