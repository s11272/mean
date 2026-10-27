import base64
from datetime import UTC, datetime
from typing import Any

import pytest

from config import Settings
from integrations.qtest.client import QTestClient
from integrations.qtest.models import (
    QTestAttachment,
    QTestLogPayload,
    QTestStepLog,
)


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


class QTestPlugin:
    def __init__(self, settings: Settings) -> None:
        self.client = QTestClient(settings)
        self._steps: dict[str, list[QTestStepLog]] = {}
        self._start_times: dict[str, str] = {}

    def _extract_tc_id(self, item: pytest.Item) -> str | None:
        for marker in item.iter_markers():
            if marker.name.startswith("qtest_"):
                return marker.name.removeprefix("qtest_")
        return None

    def pytest_runtest_setup(self, item: pytest.Item) -> None:
        if self._extract_tc_id(item):
            self._steps[item.nodeid] = []
            self._start_times[item.nodeid] = _now_iso()

    def pytest_bdd_after_step(
        self, request: pytest.FixtureRequest, step: Any
    ) -> None:
        nodeid = request.node.nodeid
        if nodeid in self._steps:
            order = len(self._steps[nodeid]) + 1
            self._steps[nodeid].append(
                QTestStepLog(
                    order=order,
                    description=f"{step.keyword} {step.name}",
                    expected_result="Step executed successfully",
                    actual_result="Passed",
                    status="PASSED",
                )
            )

    def pytest_bdd_step_error(
        self, request: pytest.FixtureRequest, step: Any, exception: Exception
    ) -> None:
        nodeid = request.node.nodeid
        if nodeid in self._steps:
            order = len(self._steps[nodeid]) + 1
            self._steps[nodeid].append(
                QTestStepLog(
                    order=order,
                    description=f"{step.keyword} {step.name}",
                    expected_result="Step executed successfully",
                    actual_result=str(exception),
                    status="FAILED",
                )
            )

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(
        self, item: pytest.Item, call: pytest.CallInfo[None]
    ) -> Any:
        outcome = yield
        report: pytest.TestReport = outcome.get_result()

        if report.when != "call":
            return

        tc_id = self._extract_tc_id(item)
        if not tc_id:
            return

        status = "PASSED" if report.passed else "FAILED"
        attachments: list[QTestAttachment] = []

        if report.failed:
            driver = item.funcargs.get("driver")
            if driver is not None:
                try:
                    raw_bytes = driver.screenshot()
                    b64_data = base64.b64encode(raw_bytes).decode("ascii")
                    attachments.append(
                        QTestAttachment(
                            name="failure.png",
                            data=b64_data,
                        )
                    )
                except Exception:
                    pass

        payload = QTestLogPayload(
            name=item.name,
            automation_content=tc_id,
            status=status,
            exe_start_date=self._start_times.get(item.nodeid, _now_iso()),
            exe_end_date=_now_iso(),
            test_step_logs=self._steps.pop(item.nodeid, []),
            attachments=attachments,
        )
        self._start_times.pop(item.nodeid, None)
        self.client.submit_test_log(payload)