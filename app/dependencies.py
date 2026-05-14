from app.shared.event_bus import EventBus
from app.telemetry.api import TelemetryModule, TelemetryRecorded
from app.analytics.api import AnalyticsModule

from app.analytics.infrastructure.repositories import SqlAlchemySensorMetricRepository
from app.analytics.application.handlers import OnTelemetryRecordedHandler
from app.analytics.acl.telemetry_translator import TelemetryEventTranslator

from app.telemetry.infrastructure.services import ConsoleAlertingService

global_event_bus = EventBus()

telemetry_module = TelemetryModule(event_bus=global_event_bus)
analytics_module = AnalyticsModule()

_analytics_event_handler = OnTelemetryRecordedHandler(
    metric_repo=SqlAlchemySensorMetricRepository(),
    translator=TelemetryEventTranslator(),
)

global_event_bus.subscribe(TelemetryRecorded, _analytics_event_handler.handle)

alerting_service = ConsoleAlertingService(threshold=80.0)
global_event_bus.subscribe(TelemetryRecorded, alerting_service.handle_telemetry_recorded)