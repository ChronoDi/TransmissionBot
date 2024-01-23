import itertools

from aiogram.fsm.context import FSMContext


async def slice_list(start_list: list, num_elements: int) -> tuple[dict[str, list], int]:
    result_dict: dict[str, list] = {}
    cursor = 0
    num_pages = len(start_list) // num_elements
    add_pager = len(start_list) % num_elements

    for i in range(0, num_pages):
        temp_dict: list = list(itertools.islice(start_list, cursor, cursor + num_elements))
        result_dict.update({str(i): temp_dict})
        cursor += num_elements

    if add_pager != 0:
        temp_dict: dict[str: str] = list(itertools.islice(start_list, cursor, len(start_list)))
        result_dict.update({str(num_pages): temp_dict})
        num_pages += 1

    if not result_dict:
        result_dict.update({str(0): {}})
        num_pages = 0

    return result_dict, num_pages


async def get_current_page_from_list(state: FSMContext, is_next: bool = True) -> list:
    data = await state.get_data()
    result_dict: dict[str, list] = data['result_dict']
    current_page = data['current_page']
    num_pages = data['num_pages']

    if num_pages == 0:
        return result_dict[str(0)]

    if is_next:
        current_page = current_page + 1 if current_page != num_pages - 1 else 0
    else:
        current_page = current_page - 1 if current_page != 0 else num_pages - 1

    await state.update_data(current_page=current_page)

    return result_dict[str(current_page)]


