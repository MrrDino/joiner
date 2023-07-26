import time

from loguru import logger

from constants import URL
from helper import read_file
from joiner import send_request


def start():
    """Функция запуска скрипта"""

    tokens = read_file("tokens.txt")
    invites = read_file("links.txt")

    for token in tokens:
        joins = 0

        for invite in invites:
            url = URL + invite
            logger.info(f"Token: {token}, link: https://discord.gg/{invite}")

            result = send_request(url=url, token=token)
            joins += 1 if result else 0
            if result:
                logger.success("Successfully joined!")
            else:
                logger.error(f"An error occurred while trying to join")
            time.sleep(10)

        logger.info(f"Token: {token}, total joins - {joins}")
        time.sleep(15)


if __name__ == "__main__":
    start()
