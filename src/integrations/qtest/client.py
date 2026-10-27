import httpx

from config import Settings
from integrations.qtest.models import QTestLogPayload


class QTestClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.base_url = \
            f"{settings.qtest_url.rstrip('/')}/api/v3/projects/{settings.qtest_project_id}"
        self.headers = {
            "Authorization": f"Bearer {settings.qtest_token}",
            "Content-Type": "application/json",
        }

    def submit_test_log(self, payload: QTestLogPayload) -> dict | None:
        url = f"{self.base_url}/auto-test-logs"
        with httpx.Client(verify=self.settings.verify_ssl) as client:
            response = client.post(
                url, json=payload.model_dump(mode="json"), headers=self.headers, timeout=30.0
            )
            response.raise_for_status()
            return response.json() if response.content else None