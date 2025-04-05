import boto3
from botocore.exceptions import ClientError
from typing import Optional, Union
import posixpath


class S3interface:
    def __init__(
        self,
        endpoint_url: str,
        access_key: str,
        secret_key: str,
        bucket_name: str
    ) -> None:
        self._bucket_name = bucket_name
        self._client = boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )

    def get_image(self, image_id: Union[int, str]) -> Optional[bytes]:
        try:
            object_key = self._generate_object_key(str(image_id))
            response = self._client.get_object(
                Bucket=self._bucket_name,
                Key=object_key
            )
            return response["Body"].read()

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code")
            if error_code == "NoSuchKey":
                return None
            raise

    def _generate_object_key(self, image_id: str) -> str:
        padded_id = image_id.zfill(len(image_id) + 1)
        prefix = padded_id[:3]
        filename = f"{padded_id}.jpg"
        print(posixpath.join(prefix, filename))
        return posixpath.join(prefix, filename)

    @property
    def bucket_name(self) -> str:
        return self._bucket_name
