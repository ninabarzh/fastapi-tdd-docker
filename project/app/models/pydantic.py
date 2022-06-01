""" project/app/models/pydantic.py
    https://pydantic-docs.helpmanual.io/usage/models/

   isort:skip_file
"""

#

from pydantic import BaseModel, AnyHttpUrl


class SummaryPayloadSchema(BaseModel):
    url: AnyHttpUrl


class SummaryResponseSchema(SummaryPayloadSchema):
    id: int


class SummaryUpdatePayloadSchema(SummaryPayloadSchema):
    summary: str
