"""Lucide icon helpers for QuantCoach.

Generates high-precision, inline Lucide SVG icons designed for quantitative workstations.
Matches Lucide's official SVG specifications.
"""

from typing import Optional

LUCIDE_PATHS: dict[str, str] = {
    "bot": (
        '<path d="M12 8V4H8"/>'
        '<rect width="16" height="12" x="4" y="8" rx="2"/>'
        '<path d="M2 14h2"/>'
        '<path d="M20 14h2"/>'
        '<path d="M15 13v2"/>'
        '<path d="M9 13v2"/>'
    ),
    "brain": (
        '<path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/>'
        '<path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/>'
        '<path d="M12 3v18"/>'
    ),
    "graduation-cap": (
        '<path d="M21.42 10.922a1 1 0 0 0-.019-.838L12.83 3.18a2 2 0 0 0-1.66 0L2.6 10.084a1 1 0 0 0 0 1.832l8.57 6.908a2 2 0 0 0 1.66 0l6.71-5.409a1 1 0 0 0 .44-.893v-1.6z"/>'
        '<path d="M6 12.5v5c0 1.66 2.69 3 6 3s6-1.34 6-3v-5"/>'
    ),
    "book-open": (
        '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>'
        '<path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>'
    ),
    "trending-up": (
        '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/>'
        '<polyline points="16 7 22 7 22 13"/>'
    ),
    "line-chart": (
        '<path d="M3 3v18h18"/>'
        '<path d="m19 9-5 5-4-4-3 3"/>'
    ),
    "video": (
        '<path d="m22 8-6 4 6 4V8Z"/>'
        '<rect width="14" height="12" x="2" y="6" rx="2"/>'
    ),
    "info": (
        '<circle cx="12" cy="12" r="10"/>'
        '<path d="M12 16v-4"/>'
        '<path d="M12 8h.01"/>'
    ),
    "settings": (
        '<path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/>'
        '<circle cx="12" cy="12" r="3"/>'
    ),
    "mic": (
        '<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/>'
        '<path d="M19 10v2a7 7 0 0 1-14 0v-2"/>'
        '<line x1="12" x2="12" y1="19" y2="22"/>'
    ),
    "volume-2": (
        '<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/>'
        '<path d="M15.54 8.46a5 5 0 0 1 0 7.07"/>'
        '<path d="M19.07 4.93a10 10 0 0 1 0 14.14"/>'
    ),
    "thumbs-up": (
        '<path d="M7 10v12"/>'
        '<path d="M15 5.88 14 10h5.83a2 2 0 0 1 1.92 2.56l-2.33 8A2 2 0 0 1 17.5 22H4a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2h3"/>'
        '<path d="M7 10a5 5 0 0 0 3-4.12V4a2 2 0 0 1 4 0v1.88"/>'
    ),
    "thumbs-down": (
        '<path d="M17 14V2"/>'
        '<path d="M9 18.12 10 14H4.17a2 2 0 0 1-1.92-2.56l2.33-8A2 2 0 0 1 6.5 2H20a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-3"/>'
        '<path d="M17 14a5 5 0 0 0-3 4.12V20a2 2 0 0 1-4 0v-1.88"/>'
    ),
    "sparkles": (
        '<path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>'
        '<path d="M5 3v4"/>'
        '<path d="M19 17v4"/>'
        '<path d="M3 5h4"/>'
        '<path d="M17 19h4"/>'
    ),
    "cpu": (
        '<rect width="16" height="16" x="4" y="4" rx="2"/>'
        '<rect width="6" height="6" x="9" y="9" rx="1"/>'
        '<path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/>'
        '<path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/>'
    ),
    "database": (
        '<ellipse cx="12" cy="5" rx="9" ry="3"/>'
        '<path d="M3 5v14c0 1.66 4.03 3 9 3s9-1.34 9-3V5"/>'
        '<path d="M3 12c0 1.66 4.03 3 9 3s9-1.34 9-3"/>'
    ),
    "code-2": (
        '<path d="m18 16 4-4-4-4"/>'
        '<path d="m6 8-4 4 4 4"/>'
        '<path d="m14.5 4-5 16"/>'
    ),
    "bar-chart-3": (
        '<path d="M3 3v18h18"/>'
        '<path d="M18 17V9"/>'
        '<path d="M13 17V5"/>'
        '<path d="M8 17v-3"/>'
    ),
    "trash-2": (
        '<path d="M3 6h18"/>'
        '<path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/>'
        '<path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>'
        '<line x1="10" x2="10" y1="11" y2="17"/>'
        '<line x1="14" x2="14" y1="11" y2="17"/>'
    ),
    "check-circle-2": (
        '<path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"/>'
        '<path d="m9 12 2 2 4-4"/>'
    ),
    "alert-circle": (
        '<circle cx="12" cy="12" r="10"/>'
        '<line x1="12" x2="12" y1="8" y2="12"/>'
        '<line x1="12" x2="12.01" y1="16" y2="16"/>'
    ),
    "layers": (
        '<polygon points="12 2 2 7 12 12 22 7 12 2"/>'
        '<polyline points="2 17 12 22 22 17"/>'
        '<polyline points="2 12 12 17 22 12"/>'
    ),
    "shield-check": (
        '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>'
        '<path d="m9 12 2 2 4-4"/>'
    ),
    "zap": (
        '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>'
    ),
    "refresh-cw": (
        '<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/>'
        '<path d="M21 3v5h-5"/>'
        '<path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/>'
        '<path d="M8 16H3v5"/>'
    ),
    "sliders": (
        '<line x1="4" x2="4" y1="21" y2="14"/>'
        '<line x1="4" x2="4" y1="10" y2="3"/>'
        '<line x1="12" x2="12" y1="21" y2="12"/>'
        '<line x1="12" x2="12" y1="8" y2="3"/>'
        '<line x1="20" x2="20" y1="21" y2="16"/>'
        '<line x1="20" x2="20" y1="12" y2="3"/>'
        '<line x1="1" x2="7" y1="14" y2="14"/>'
        '<line x1="9" x2="15" y1="8" y2="8"/>'
        '<line x1="17" x2="23" y1="16" y2="16"/>'
    ),
    "play": (
        '<polygon points="6 3 20 12 6 21 6 3"/>'
    ),
    "compass": (
        '<circle cx="12" cy="12" r="10"/>'
        '<polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>'
    ),
    "activity": (
        '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>'
    ),
    "flame": (
        '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/>'
    ),
    "target": (
        '<circle cx="12" cy="12" r="10"/>'
        '<circle cx="12" cy="12" r="6"/>'
        '<circle cx="12" cy="12" r="2"/>'
    ),
    "award": (
        '<circle cx="12" cy="8" r="6"/>'
        '<path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"/>'
    )
}


def lucide_icon(
    name: str,
    size: int = 20,
    color: str = "currentColor",
    stroke_width: float = 2.0,
    class_name: str = "",
    style: str = "",
) -> str:
    """Return an inline SVG string for the specified Lucide icon."""
    path_content = LUCIDE_PATHS.get(name.lower(), LUCIDE_PATHS["activity"])
    extra_style = f"style='{style}'" if style else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" '
        f'stroke-linecap="round" stroke-linejoin="round" '
        f'class="lucide lucide-{name} {class_name}" {extra_style}>'
        f'{path_content}'
        f'</svg>'
    )


def icon_badge(
    icon_name: str,
    text: str,
    icon_color: str = "#991B1B",
    bg_color: str = "rgba(153, 27, 27, 0.08)",
    border_color: str = "rgba(153, 27, 27, 0.22)",
    text_color: str = "#7F1D1D",
    size: int = 14,
) -> str:
    """Return a styled pill badge with an inline Lucide icon."""
    svg = lucide_icon(icon_name, size=size, color=icon_color, stroke_width=2.2)
    return (
        f'<span style="display: inline-flex; align-items: center; gap: 6px; '
        f'background: {bg_color}; border: 1px solid {border_color}; '
        f'color: {text_color}; border-radius: 9999px; padding: 4px 12px; '
        f'font-size: 0.78rem; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase;">'
        f'{svg}<span>{text}</span></span>'
    )


def section_header_html(
    icon_name: str,
    title: str,
    subtitle: Optional[str] = None,
    icon_color: str = "#991B1B",
) -> str:
    """Return an editorial section header with a Lucide icon."""
    svg = lucide_icon(icon_name, size=24, color=icon_color, stroke_width=2.2)
    sub_html = f'<p class="section-subtitle">{subtitle}</p>' if subtitle else ""
    return (
        f'<div class="section-header-block">'
        f'  <div class="section-heading">'
        f'    <div class="section-icon-wrap">{svg}</div>'
        f'    <h2>{title}</h2>'
        f'  </div>'
        f'  {sub_html}'
        f'</div>'
    )
