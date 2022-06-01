""" project/app/api/summaries.py
    https://fastapi.tiangolo.com/tutorial/body/

   isort:skip_file
"""

from typing import List

from fastapi import APIRouter, HTTPException, Path, BackgroundTasks

from app.api import crud
from app.models.pydantic import (
    SummaryPayloadSchema,
    SummaryResponseSchema,
    SummaryUpdatePayloadSchema,
)
from app.models.tortoise import SummarySchema
from app.summarizer import generate_summary


SUMMARY_NOT_FOUND_MSG = "Summary not found"

router = APIRouter()


@router.post("/", response_model=SummaryResponseSchema, status_code=201)
async def create_summary(
    payload: SummaryPayloadSchema, background_tasks: BackgroundTasks
) -> SummaryResponseSchema:
    summary_id = await crud.post(payload)

    background_tasks.add_task(generate_summary, summary_id, payload.url)

    response_object = {"id": summary_id, "url": payload.url}
    return response_object


@router.get("/{id}/", response_model=SummarySchema)
async def read_summary(id: int = Path(..., gt=0)) -> SummarySchema:
    summary = await crud.get(id)
    if not summary:
        raise HTTPException(status_code=404, detail=SUMMARY_NOT_FOUND_MSG)

    return summary


@router.get("/", response_model=List[SummarySchema])
async def read_all_summaries() -> List[SummarySchema]:
    return await crud.get_all()


@router.delete("/{id}/", response_model=SummaryResponseSchema)
async def delete_summary(id: int) -> SummaryResponseSchema:
    summary = await crud.get(id)
    if not summary:
        raise HTTPException(status_code=404, detail=SUMMARY_NOT_FOUND_MSG)

    await crud.delete(id)

    return summary


@router.put("/{id}/", response_model=SummarySchema)
async def update_summary(
    payload: SummaryUpdatePayloadSchema, id: int = Path(..., gt=0)
) -> SummarySchema:
    summary = await crud.put(id, payload)
    if not summary:
        raise HTTPException(status_code=404, detail=SUMMARY_NOT_FOUND_MSG)

    return summary
