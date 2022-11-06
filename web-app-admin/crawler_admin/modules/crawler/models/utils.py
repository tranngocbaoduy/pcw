import uuid


def id_gen(ID_LENGTH=6) -> str:
    """Generates random string whose length is `ID_LENGTH`"""
    return str(uuid.uuid4().int)[:ID_LENGTH]
