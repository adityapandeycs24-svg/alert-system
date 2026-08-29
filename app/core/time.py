from datetime import datetime, timezone

def utc_now() -> datetime:
    """Returns timezone-aware UTC datetime for the current moment."""
    return datetime.now(timezone.utc)

def format_utc_iso(dt: datetime | None) -> str | None:
    """Formats datetime to ISO 8601 string with 'Z' suffix (e.g. 2026-08-26T10:32:15Z)."""
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    # Format with 'Z' suffix instead of +00:00
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
