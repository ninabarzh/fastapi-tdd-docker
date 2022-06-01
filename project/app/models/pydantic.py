# project/app/models/pydantic.py
# https://pydantic-docs.helpmanual.io/usage/models/

from pydantic import BaseModel


class SummaryPayloadSchema(BaseModel):
    url: str


class SummaryResponseSchema(SummaryPayloadSchema):
    id: int
