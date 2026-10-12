"""Regression tests for the image capability gate on pre-formatted messages."""

import pytest

from prometheus.providers.base import ApiMessageRequest
from prometheus.providers.stub import UnsupportedContentBlock, _build_openai_messages


@pytest.mark.parametrize("part_type", ["image_url", "input_image", "image"])
def test_preformatted_image_is_rejected_without_declared_vision(part_type: str) -> None:
    message = {
        "role": "user",
        "content": [
            {"type": "text", "text": "Describe this picture."},
            {
                "type": part_type,
                "image_url": {"url": "data:image/png;base64,AAAA"},
            },
        ],
    }

    request = ApiMessageRequest(model="text-only-model", messages=[message])

    with pytest.raises(UnsupportedContentBlock, match="pre-formatted 'user' messages"):
        _build_openai_messages(request, allow_images=False)


def test_preformatted_image_is_preserved_when_vision_is_declared() -> None:
    message = {
        "role": "user",
        "content": [
            {"type": "text", "text": "Describe this picture."},
            {
                "type": "image_url",
                "image_url": {"url": "data:image/png;base64,AAAA"},
            },
        ],
    }

    request = ApiMessageRequest(model="vision-model", messages=[message])

    assert _build_openai_messages(request, allow_images=True) == [message]


def test_preformatted_text_message_still_passes_without_vision() -> None:
    message = {"role": "user", "content": "Hello"}

    request = ApiMessageRequest(model="text-only-model", messages=[message])

    assert _build_openai_messages(request, allow_images=False) == [message]
