from app.services import timestamp


class ReturnErrorMSG:
    """

    result:
        {
            "status": bool,
            "system": {
                "code": int,
                "message": str
            },
            "data": None,
        }
    """
    def __init__(self, status: bool, code: int, message: str) -> None:
        self.__dict__.update(
            {
                "status": status,
                "system": {
                    "code": code,
                    "message": message
                },
                "data": None,
                "timestamp": timestamp()
            }
        )
