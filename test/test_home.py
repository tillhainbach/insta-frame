"""Test home route."""


from flask import Flask
from werkzeug import Response
from werkzeug.datastructures import FileStorage

cat_image = FileStorage(
    stream=open("test/__fixtures__/cat.jpeg", "rb"),
    filename="cat.jpeg",
    content_type="image/jpg",
)


def test_upload_image(client: Flask) -> None:
    """Test an image can be uploaded."""

    response: Response = client.get("/")  # type: ignore

    assert b"Upload new File" in response.data

    response: Response = client.post(
        "/",
        data={"file": cat_image},
        follow_redirects=True,
        content_type="multipart/form-data",
    )  # type: ignore

    assert response.status_code == 200
    assert "cat.jpeg" in response.headers["Content-Disposition"]
