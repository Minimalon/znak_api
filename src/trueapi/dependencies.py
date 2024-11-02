from fastapi import Depends

async def correct_paramds(**kwargs):
    return {key: value for key, value in kwargs.items() if value is not None}