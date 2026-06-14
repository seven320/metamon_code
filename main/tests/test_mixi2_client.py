import pytest

from src.mixi2_client import Mixi2Client

from social.mixi.application.service.application_api.v1 import service_pb2


@pytest.fixture
def client(mocker):
    token_provider = mocker.Mock()
    token_provider.token.return_value = "tok"
    c = Mixi2Client(
        api_address="api:443", token_provider=token_provider, channel=mocker.Mock()
    )
    c._stub = mocker.Mock()
    return c


class Test_upload_image:
    def test_uploads_and_polls_until_completed(self, client, mocker, tmp_path):
        client._stub.InitiatePostMediaUpload.return_value = mocker.Mock(
            media_id="m1", upload_url="https://upload.example/x"
        )
        S = service_pb2.GetPostMediaStatusResponse
        client._stub.GetPostMediaStatus.side_effect = [
            mocker.Mock(status=S.STATUS_PROCESSING),
            mocker.Mock(status=S.STATUS_COMPLETED),
        ]
        post = mocker.patch("src.mixi2_client.requests.post")
        post.return_value = mocker.Mock(status_code=202)
        mocker.patch("src.mixi2_client.time.sleep")

        img = tmp_path / "erai.png"
        img.write_bytes(b"\x89PNG\r\n")

        media_id = client.upload_image(str(img))

        assert media_id == "m1"
        # POST に画像バイト・Content-Type・Bearer が渡る（実機検証: PUT/multipart は不可）
        _, kwargs = post.call_args
        assert kwargs["data"] == b"\x89PNG\r\n"
        assert kwargs["headers"]["Content-Type"] == "image/png"
        assert kwargs["headers"]["Authorization"] == "Bearer tok"
        # initiate に正しいサイズ/種別
        req = client._stub.InitiatePostMediaUpload.call_args[0][0]
        assert req.data_size == 6
        assert req.media_type == service_pb2.InitiatePostMediaUploadRequest.TYPE_IMAGE
        assert client._stub.GetPostMediaStatus.call_count == 2

    def test_raises_on_failed_status(self, client, mocker, tmp_path):
        client._stub.InitiatePostMediaUpload.return_value = mocker.Mock(
            media_id="m1", upload_url="https://upload.example/x"
        )
        S = service_pb2.GetPostMediaStatusResponse
        client._stub.GetPostMediaStatus.return_value = mocker.Mock(
            status=S.STATUS_FAILED
        )
        mocker.patch("src.mixi2_client.requests.post").return_value = mocker.Mock(
            status_code=202
        )
        mocker.patch("src.mixi2_client.time.sleep")
        img = tmp_path / "x.png"
        img.write_bytes(b"x")
        with pytest.raises(RuntimeError):
            client.upload_image(str(img))

    def test_raises_on_upload_http_error(self, client, mocker, tmp_path):
        client._stub.InitiatePostMediaUpload.return_value = mocker.Mock(
            media_id="m1", upload_url="https://upload.example/x"
        )
        mocker.patch("src.mixi2_client.requests.post").return_value = mocker.Mock(
            status_code=403, text="denied"
        )
        img = tmp_path / "x.png"
        img.write_bytes(b"x")
        with pytest.raises(RuntimeError):
            client.upload_image(str(img))
