from unittest.mock import MagicMock, patch, call
import pytest

from app.application.commands import RecordTelemetryCommand
from app.application.handlers import (
    RecordTelemetryCommandHandler,
    RecordTelemetryCommandHandlerSync,
)
from app.domain.exceptions import DomainError
from app.domain.services import IAlertingService
from app.domain.events import TelemetryRecorded
from app.infrastructure.services import ConsoleAlertingService
from app.infrastructure.event_bus import EventBus


def make_sensor_repo(found: bool = True):
    repo = MagicMock()
    repo.get_by_id.return_value = MagicMock() if found else None
    return repo

def make_telemetry_repo():
    return MagicMock()


# ConsoleAlertingService

def test_alerting_service_prints_when_above_threshold():
    service = ConsoleAlertingService(threshold=80.0)
    with patch("builtins.print") as mock_print:
        service.check_and_alert(sensor_id=1, value=85.0)
        mock_print.assert_called_once()


def test_alerting_service_silent_when_below_threshold():
    service = ConsoleAlertingService(threshold=80.0)
    with patch("builtins.print") as mock_print:
        service.check_and_alert(sensor_id=1, value=50.0)
        mock_print.assert_not_called()


def test_alerting_service_silent_on_exact_threshold():
    service = ConsoleAlertingService(threshold=80.0)
    with patch("builtins.print") as mock_print:
        service.check_and_alert(sensor_id=1, value=80.0)
        mock_print.assert_not_called()


def test_handle_telemetry_recorded_delegates_to_check():
    service = ConsoleAlertingService(threshold=80.0)
    event = TelemetryRecorded(sensor_id=7, value=95.0, happened_at=None)
    with patch("builtins.print") as mock_print:
        service.handle_telemetry_recorded(event)
        mock_print.assert_called_once()


# Синхронний handler

def test_sync_handler_calls_alerting_service_directly():
    alerting = MagicMock(spec=IAlertingService)
    handler = RecordTelemetryCommandHandlerSync(
        telemetry_repo=make_telemetry_repo(),
        sensor_repo=make_sensor_repo(found=True),
        alerting_service=alerting,
    )
    handler.handle(RecordTelemetryCommand(sensor_id=1, value=90.0))
    alerting.check_and_alert.assert_called_once_with(sensor_id=1, value=90.0)


def test_sync_handler_saves_telemetry_even_if_alerting_fails():
    alerting = MagicMock(spec=IAlertingService)
    alerting.check_and_alert.side_effect = Exception("Alert service is down")

    telemetry_repo = make_telemetry_repo()

    handler = RecordTelemetryCommandHandlerSync(
        telemetry_repo=telemetry_repo,
        sensor_repo=make_sensor_repo(found=True),
        alerting_service=alerting,
    )
    handler.handle(RecordTelemetryCommand(sensor_id=1, value=90.0))

    telemetry_repo.save.assert_called_once()


def test_sync_handler_raises_if_sensor_not_found():
    alerting = MagicMock(spec=IAlertingService)
    handler = RecordTelemetryCommandHandlerSync(
        telemetry_repo=make_telemetry_repo(),
        sensor_repo=make_sensor_repo(found=False),
        alerting_service=alerting,
    )
    with pytest.raises(DomainError):
        handler.handle(RecordTelemetryCommand(sensor_id=999, value=50.0))


# Асинхронний handler 

def test_async_handler_publishes_event_after_save():
    event_bus = EventBus()
    subscriber = MagicMock()
    event_bus.subscribe(TelemetryRecorded, subscriber)

    handler = RecordTelemetryCommandHandler(
        telemetry_repo=make_telemetry_repo(),
        sensor_repo=make_sensor_repo(found=True),
        event_bus=event_bus,
    )
    handler.handle(RecordTelemetryCommand(sensor_id=2, value=90.0))

    subscriber.assert_called_once()
    event: TelemetryRecorded = subscriber.call_args[0][0]
    assert event.sensor_id == 2
    assert event.value == 90.0


def test_async_handler_telemetry_saved_even_if_subscriber_fails():
    event_bus = EventBus()
    event_bus.subscribe(TelemetryRecorded, MagicMock(side_effect=Exception("subscriber down")))

    telemetry_repo = make_telemetry_repo()

    handler = RecordTelemetryCommandHandler(
        telemetry_repo=telemetry_repo,
        sensor_repo=make_sensor_repo(found=True),
        event_bus=event_bus,
    )

    with pytest.raises(Exception, match="subscriber down"):
        handler.handle(RecordTelemetryCommand(sensor_id=2, value=90.0))

    telemetry_repo.save.assert_called_once()


def test_async_handler_does_not_know_about_alerting_service():

    import inspect
    sig = inspect.signature(RecordTelemetryCommandHandler.__init__)
    param_names = list(sig.parameters.keys())
    assert "alerting_service" not in param_names


def test_async_handler_raises_if_sensor_not_found():
    handler = RecordTelemetryCommandHandler(
        telemetry_repo=make_telemetry_repo(),
        sensor_repo=make_sensor_repo(found=False),
        event_bus=EventBus(),
    )
    with pytest.raises(DomainError):
        handler.handle(RecordTelemetryCommand(sensor_id=999, value=50.0))