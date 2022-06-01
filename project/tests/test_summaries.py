""" project/tests/test_summaries.py

   isort:skip_file
"""

import json
import pytest


URL = "https://foo.bar"
SUMMARIES_ROUTE = "/summaries/"
FIELD_REQUIRED_MSG = "field required"
MISSING_VALUE_ERROR_MSG = "value_error.missing"
SUMMARIES_ID_999_ROUTE = "/summaries/999/"
SUMMARY_NOT_FOUND_MSG = "Summary not found"
UPDATED_MSG = "updated!"


def test_create_summary(test_app_with_db):
    # Given: test_app_with_db
    # When:
    response = test_app_with_db.post(SUMMARIES_ROUTE, data=json.dumps({"url": URL}))

    # Then:
    assert response.status_code == 201
    assert response.json()["url"] == URL


def test_create_summaries_invalid_json(test_app):
    # Given: test_app
    # When:
    response = test_app.post(SUMMARIES_ROUTE, data=json.dumps({}))

    # Then:
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

    # When
    response = test_app.post(SUMMARIES_ROUTE, data=json.dumps({"url": "invalid://url"}))
    # Then
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "URL scheme not permitted"


def test_read_summary(test_app_with_db):
    # Given: test_app_with_db
    response = test_app_with_db.post(SUMMARIES_ROUTE, data=json.dumps({"url": URL}))
    summary_id = response.json()["id"]

    # When:
    response = test_app_with_db.get(f"/summaries/{summary_id}/")
    # Then:
    assert response.status_code == 200

    # When:
    response_dict = response.json()
    # Then:
    assert response_dict["id"] == summary_id
    assert response_dict["url"] == URL
    assert response_dict["summary"]
    assert response_dict["created_at"]


def test_read_summary_incorrect_id(test_app_with_db):
    # Given: test_app_with_db
    # When:
    response = test_app_with_db.get(SUMMARIES_ID_999_ROUTE)
    # Then:
    assert response.status_code == 404
    assert response.json()["detail"] == SUMMARY_NOT_FOUND_MSG

    # When:
    response = test_app_with_db.get("/summaries/0/")
    # Then:
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["path", "id"],
                "msg": "ensure this value is greater than 0",
                "type": "value_error.number.not_gt",
                "ctx": {"limit_value": 0},
            }
        ]
    }


def test_read_all_summaries(test_app_with_db):
    # Given: test_app_with_db
    response = test_app_with_db.post(SUMMARIES_ROUTE, data=json.dumps({"url": URL}))
    summary_id = response.json()["id"]

    # When:
    response = test_app_with_db.get(SUMMARIES_ROUTE)
    # Then:
    assert response.status_code == 200

    # When
    response_list = response.json()
    # Then
    assert len(list(filter(lambda d: d["id"] == summary_id, response_list))) == 1


def test_remove_summary(test_app_with_db):
    # Given: test_app_with_db
    response = test_app_with_db.post(SUMMARIES_ROUTE, data=json.dumps({"url": URL}))
    summary_id = response.json()["id"]

    # When:
    response = test_app_with_db.delete(f"/summaries/{summary_id}/")
    # Then:
    assert response.status_code == 200
    assert response.json() == {"id": summary_id, "url": URL}


def test_remove_summary_incorrect_id(test_app_with_db):
    # Given: test_app_with_db
    # When:
    response = test_app_with_db.delete(SUMMARIES_ID_999_ROUTE)
    # Then:
    assert response.status_code == 404
    assert response.json()["detail"] == SUMMARY_NOT_FOUND_MSG


def test_update_summary(test_app_with_db):
    # Given: test_app_with_db
    response = test_app_with_db.post("/summaries/", data=json.dumps({"url": URL}))
    summary_id = response.json()["id"]

    # When:
    response = test_app_with_db.put(
        f"/summaries/{summary_id}/",
        data=json.dumps({"url": URL, "summary": UPDATED_MSG}),
    )
    # Then:
    assert response.status_code == 200

    # When:
    response_dict = response.json()
    # Then:
    assert response_dict["id"] == summary_id
    assert response_dict["url"] == URL
    assert response_dict["summary"] == UPDATED_MSG
    assert response_dict["created_at"]


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
def test_update_summary_invalid(
    test_app_with_db, summary_id, payload, status_code, detail
):
    response = test_app_with_db.put(
        f"/summaries/{summary_id}/", data=json.dumps(payload)
    )
    assert response.status_code == status_code
    assert response.json()["detail"] == detail


def test_update_summary_invalid_url(test_app):
    response = test_app.put(
        "/summaries/1/",
        data=json.dumps({"url": "invalid://url", "summary": UPDATED_MSG}),
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "URL scheme not permitted"
