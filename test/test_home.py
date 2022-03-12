"""Test home route."""

import io

import pytest
from quart.datastructures import FileStorage
from quart.testing import QuartClient
from syrupy.assertion import SnapshotAssertion
from syrupy.extensions.json import JSONSnapshotExtension


@pytest.mark.asyncio
async def test_home_route(
    client: QuartClient, html_snapshot: SnapshotAssertion
) -> None:
    response = await client.get("/")

    assert response.status_code == 200

    assert await response.get_data() == html_snapshot


@pytest.mark.asyncio
async def test_upload_image(client: QuartClient, snapshot: SnapshotAssertion) -> None:
    files = {
        "file": FileStorage(
            stream=open("test/__fixtures__/cat.jpg", "rb"),
            filename="cat.jpg",
            content_type="image/jpg",
        )
    }

    response = await client.post("/%3F", files=files)
    print(response.status)
    json = await response.get_json()

    assert json == snapshot(extension_class=JSONSnapshotExtension)


no_filename = {
    "file": FileStorage(
        stream=io.BytesIO(b"abcdefgh"),
        filename="",
        content_type="image/jpg",
    )
}

no_image = {
    "file": FileStorage(
        stream=io.BytesIO(b"abcdefgh"),
        filename="image.txt",
        content_type="image/jpg",
    )
}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["files", "flash"],
    [
        (None, b"Uploaded content is not an image!"),
        (no_filename, b"No file part!"),
        (no_image, b"Could not recognize uploaded file as an image!"),
    ],
)
async def test_upload_image_fails(client: QuartClient, files, flash: bytes) -> None:
    response = await client.post("/%3F", files=files)
    json = await response.get_json()

    assert json["image"] is None

    response = await client.get("/")

    assert response.status_code == 200
    assert flash in await response.get_data(as_text=False)
