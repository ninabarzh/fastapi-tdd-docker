""" project/tests/test_summaries_unit.py

   isort:skip_file
"""

import json
from datetime import datetime

import pytest

from app.api import crud, summaries


URL = "https://foo.bar"
SUMMARIES_ROUTE = "/summaries/"
FIELD_REQUIRED_MSG = "field required"
MISSING_VALUE_ERROR_MSG = "value_error.missing"
SUMMARIES_ID_999_ROUTE = "/summaries/999/"
SUMMARIES_ID_1_ROUTE = "/summaries/1/"
SUMMARY_NOT_FOUND_MSG = "Summary not found"
UPDATED_MSG = "updated!"


def test_create_summary(test_app, monkeypatch):
    test_request_payload = {"url": URL}
    test_response_payload = {"id": 1, "url": URL}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post(SUMMARIES_ROUTE, data=json.dumps(test_request_payload),)

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_summaries_invalid_json(test_app):
    response = test_app.post(SUMMARIES_ROUTE, data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "url"],
                "msg": FIELD_REQUIRED_MSG,
                "type": MISSING_VALUE_ERROR_MSG,
            }
        ]
    }

    response = test_app.post(SUMMARIES_ROUTE, data=json.dumps({"url": "invalid://url"}))
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "URL scheme not permitted"


def test_read_summary(test_app, monkeypatch):
    test_data = {
        "id": 1,
        "url": URL,
        "summary": "summary",
        "created_at": datetime.utcnow().isoformat(),
    }

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get(SUMMARIES_ID_1_ROUTE)
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_summary_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get(SUMMARIES_ID_999_ROUTE)
    assert response.status_code == 404
    assert response.json()["detail"] == SUMMARY_NOT_FOUND_MSG


def test_read_all_summaries(test_app, monkeypatch):
    test_data = [
        {
            "id": 1,
            "url": URL,
            "summary": "summary",
            "created_at": datetime.utcnow().isoformat(),
        },
        {
            "id": 2,
            "url": "https://testdrivenn.io",
            "summary": "summary",
            "created_at": datetime.utcnow().isoformat(),
        }
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get(SUMMARIES_ROUTE)
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_summary(test_app, monkeypatch):
    async def mock_get(id):
        return {
            "id": 1,
            "url": URL,
            "summary": "summary",
            "created_at": datetime.utcnow().isoformat(),
        }

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete(SUMMARIES_ID_1_ROUTE)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "url": URL}


def test_remove_summary_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete(SUMMARIES_ID_999_ROUTE)
    assert response.status_code == 404
    assert response.json()["detail"] == SUMMARY_NOT_FOUND_MSG


def test_update_summary(test_app, monkeypatch):
    test_request_payload = {"url": URL, "summary": "updated"}
    test_response_payload = {
        "id": 1,
        "url": URL,
        "summary": "summary",
        "created_at": datetime.utcnow().isoformat(),
    }

    async def mock_put(id, payload):
        return test_response_payload

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put(SUMMARIES_ID_1_ROUTE, data=json.dumps(test_request_payload),)
    assert response.status_code == 200
    assert response.json() == test_response_payload


@pytest.mark.parametrize(
    "summary_id, payload, status_code, detail",
    [
        [
            999,
            {"url": URL, "summary": UPDATED_MSG},
            404,
            SUMMARY_NOT_FOUND_MSG,
        ],
        [
            0,
            {"url": URL, "summary": UPDATED_MSG},
            422,
            [
                {
                    "loc": ["path", "id"],
                    "msg": "ensure this value is greater than 0",
                    "type": "value_error.number.not_gt",
                    "ctx": {"limit_value": 0},
                }
            ],
        ],
        [
            1,
            {},
            422,
            [
                {
                    "loc": ["body", "url"],
                    "msg": FIELD_REQUIRED_MSG,
                    "type": MISSING_VALUE_ERROR_MSG,
                },
                {
                    "loc": ["body", "summary"],
                    "msg": FIELD_REQUIRED_MSG,
                    "type": MISSING_VALUE_ERROR_MSG,
                },
            ],
        ],
        [
            1,
            {"url": URL},
            422,
            [
                {
                    "loc": ["body", "summary"],
                    "msg": FIELD_REQUIRED_MSG,
                    "type": MISSING_VALUE_ERROR_MSG,
                }
            ],
        ],
    ],
)
def test_update_summary_invalid(test_app, monkeypatch, summary_id, payload, status_code, detail):
    async def mock_put(id, payload):
        return None

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put(f"/summaries/{summary_id}/", data=json.dumps(payload))
    assert response.status_code == status_code
    assert response.json()["detail"] == detail


def test_update_summary_invalid_url(test_app):
    response = test_app.put(
        f"/summaries/1/",
        data=json.dumps({"url": "invalid://url", "summary": UPDATED_MSG}),
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "URL scheme not permitted"
