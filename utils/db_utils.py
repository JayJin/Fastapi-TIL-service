from sqlalchemy import inspect

def row_to_dict(row) -> dict:
    """SQLAlchey 모듈에서 제공하는 inspect 함수를 사용하여 sqlalchemy의 row의 속성을 dict로 변환."""
    return {key: getattr(row, key) for key in inspect(row).attrs.keys()}
