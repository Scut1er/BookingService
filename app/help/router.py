import ast
import csv
import io
import time
from datetime import datetime
from random import random

from fastapi import APIRouter, UploadFile
from sqlalchemy import MetaData, Table, insert, Integer, inspect, Date, ARRAY, JSON

from app.database import async_session_maker, Base
from app.exceptions import IncorrectFormatFile, TableNotFound

router = APIRouter(
    prefix="/test",
    tags=["Тестирование"]
)


def convert_value(column_type, value):
    """
    Преобразует значение в соответствующий тип на основе типа столбца.
    """
    if isinstance(value, str):
        if isinstance(column_type, Integer):
            return int(value)
        elif isinstance(column_type, Date):
            return datetime.strptime(value, '%Y-%m-%d').date()
        elif isinstance(column_type, JSON):
            return ast.literal_eval(value)
    return value


@router.post("/import/{table_name}")
async def import_data(table_name: str, csv_file: UploadFile):
    if not csv_file.filename.endswith('.csv'):
        raise IncorrectFormatFile
    data = await csv_file.read()
    reader = csv.DictReader(io.StringIO(data.decode('utf-8')), delimiter=';')
    data = [row for row in reader]

    table_model = None
    for cls in Base.__subclasses__():
        if cls.__tablename__ == table_name:
            table_model = cls
            break

    if table_model is None:
        raise TableNotFound.detail(f"Table {table_name} not found in the database.")

    async with async_session_maker() as session:
        mapper = inspect(table_model)
        columns = {column.name: column.type for column in mapper.columns}

        for item in data:
            for key, value in item.items():
                if key in columns:
                    column_type = columns[key]
                    item[key] = convert_value(column_type, value)

        stmt = insert(table_model).values(data)
        await session.execute(stmt)
        await session.commit()

        return {"status": "success", "rows_inserted": len(data)}


@router.get("/get_error")
def get_error():
    if random() > 0.5:
        raise ZeroDivisionError
    else:
        raise KeyError


@router.get("/time_consumer")
def time_consumer():
    time.sleep(random() * 5)
    return 1


@router.get("/memory_consumer")
def memory_consumer():
    _ = [i for i in range(30_000_000)]
    return 1
