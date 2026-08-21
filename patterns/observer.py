from abc import ABC, abstractmethod


# ---- Observer interface (matches lecture's Observer) ----
class Observer(ABC):
    @abstractmethod
    def update(self, event: str, payload: dict):
        pass


# ---- Subject (matches lecture's Subject, e.g. WeatherStation) ----
class ApplicationStatusSubject:
    def __init__(self):
        self._observers = []

    def register_observer(self, observer: Observer):
        self._observers.append(observer)

    def unregister_observer(self, observer: Observer):
        self._observers.remove(observer)

    def notify_observers(self, event: str, payload: dict):
        for observer in self._observers:
            observer.update(event, payload)


# ---- Concrete Observers ----
class CandidateNotifier(Observer):
    """Notifies the candidate their application status changed."""
    def update(self, event: str, payload: dict):
        message = f"[Notification] Your application for '{payload['jobTitle']}' is now: {payload['status']}"
        print(message)  # placeholder for a real notification system
        # In a real system, this could insert into a Notifications table,
        # send an email, etc. — kept simple here since it's out of scope.


class PlatformStatsLogger(Observer):
    """Logs status changes for platform-wide stats (matches SuperAdmin's viewPlatformStats)."""
    def update(self, event: str, payload: dict):
        print(f"[Stats] Event logged: {event} — status={payload['status']}")


# ---- Singleton-style access so the same Subject is reused everywhere ----
_application_subject = ApplicationStatusSubject()
_application_subject.register_observer(CandidateNotifier())
_application_subject.register_observer(PlatformStatsLogger())


def get_application_subject() -> ApplicationStatusSubject:
    return _application_subject