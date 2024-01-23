from keyboards.fabric import get_inline_keyboards


def get_pagination_keyboard(width: int = 2):
    callback_names = {'previous': '<<', 'next': '>>'}

    return get_inline_keyboards(width=width, callback_names=callback_names)
