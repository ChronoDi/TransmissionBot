from .dict import Dict

ru = Dict(
    validate_error='Вы не авторизованны!',
    start='Выберете меню:',
    transmission='Transmission',
    main_menu='Главное меню',
    download='Скачать',
    look_files='Просмотреть файлы',
    select_folder='Выберете папку:',
    films='Фильмы',
    serials='Сериалы',
    another='Другое',
    take_url_file='Введите ссылку или пришлите файл:',
    wrong_folder='Неверное название папки, попробуйте снова.',
    move='Переместить',
    delete='Удалить',
    correct_url='Ссылка принята.',
    incorrect_url='Неверная ссылка, попробуйте другую.',
    correct_file='Файл принят.',
    incorrect_file='Неверный файл, попробуйте другой.',
    torrent_view=('Торрент {id}\n'
                  'Имя: {name}\n'
                  'Скачан на {available}%\n'
                  'Лежит в папке {dir}\n\n'),
    torrent_id='Введите номер торрента:',
    torrents_id_to_remove='Введите номера торрентов через запятую',
    torrent_not_found='Торрент(ы) не найден(ы)',
    torrent_wrong_input='Неверный ввод. Попробуйте снова.',
    torrent_delete_accept='Вы точно хотите удалить эти торренты?',
    torrent_list='Список торрентов:',
    torrent_file_removed='Файл(ы) удален(ы).',
    torrent_cancel_delete='Удаление отменено.',
    torrent_move_accept='Вы точно хотите переместить торрент: "{name}" в папку "{dir}"',
    torrent_file_moved='Файл "{name}" перемещен.',
    torrent_cancel_move='Перемещение отменено.',
    torrent_here='Торрент уже в этой папке.',
    admin_echo='Я не понимаю',
    yes='Да',
    no='Нет')
