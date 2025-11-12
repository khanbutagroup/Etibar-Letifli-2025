from django import template
register = template.Library()

@register.filter
def format_duration(minutes):
    if not minutes:
        return "—"

    try:
        minutes = int(minutes)
    except ValueError:
        return str(minutes)

    hours = minutes // 60
    mins = minutes % 60

    if hours > 0 and mins > 0:
        return f"{hours} s {mins} dəq"
    elif hours > 0:
        return f"{hours} s"
    else:
        return f"{mins} dəq"
