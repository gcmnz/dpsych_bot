from datetime import datetime

from .utils import char_to_digit


def count_date_to_digit(data: str) -> int:
    result_num: int = 0

    for i in data:
        if not i.isdigit():
            continue

        result_num += int(i)

    result_str: str = str(result_num)

    if len(result_str) == 1:
        return int(result_str)

    return count_date_to_digit(result_str)


def count_vector_zhizni(chislo_deystviya: int) -> int:
    return count_date_to_digit(str(chislo_deystviya * 2 - 1))


def count_lichniy_god(dd_mm_of_birth: str) -> int:
    current_year: int = datetime.now().year
    return count_date_to_digit(f'{dd_mm_of_birth}{current_year}')


def count_name_energy_digit(name: str) -> int:
    result: int = 0
    for char in name.upper():
        result += char_to_digit[char]

    return count_date_to_digit(str(result))


def get_nomer_zadachi_ot_tvortsa(chislo_soznaniya: int) -> int:
    if chislo_soznaniya == 1:
        chislo_soznaniya = 10

    return chislo_soznaniya - 1


def get_energy_matrix(date_of_birth: str) -> list[int]:
    result: list[int] = [0] * 9
    for i in range(1, 10):
        result[i-1] = date_of_birth.count(str(i))

    return result


def get_net_energy_nums_by_matrix(energy_matrix: list[int]) -> list[int]:
    result: list[int] = []

    for i, j in enumerate(energy_matrix):
        if j == 0:
            result.append(i+1)

    return result


if __name__ == '__main__':
    pass
    # en_mat = get_energy_matrix('27.13.1988')
    # print(en_mat)
    # print(get_net_energy_nums_by_matrix(en_mat))

    # for i in range(1, 10):
    #     print(get_nomer_zadachi_ot_tvortsa(i))
    # print(count_name_energy_digit('yana'))
    # print(count_date_to_digit('07'))
    # print(count_date_to_digit('07.10.1988'))
    # print(count_date_to_digit('08.04.2022'))
    # print(count_date_to_digit('31.12.2005'))
    # print(count_date_to_digit('31.12.1991'))
    # print(count_date_to_digit('00'))
    # print(count_date_to_digit('22.09.1990'))
    # print(count_date_to_digit('11.23.1990'))

    # for i in range(1, 10):
    #     print(count_vector_zhizni(i))
