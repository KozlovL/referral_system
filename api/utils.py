import uuid

from api.constants import INVITE_CODE_MAX_LEN


def generate_invite_code():
    # Генерируем UUID4 и берем первые 6 символов
    return str(uuid.uuid4()).replace('-', '')[:INVITE_CODE_MAX_LEN]
