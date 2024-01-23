import datetime


def logging(report: str, is_error: bool = False) -> None:
    now = datetime.datetime.now().strftime("[%d-%m-%Y %H:%M:%S]")

    if not is_error:
        log = open('files/logs/events.txt', 'a', encoding="utf-8")
    else:
        log = open('files/logs/id_list.txt', 'a', encoding="utf-8")

    log.write(now + ' ' + report + '\n')
    log.close()
