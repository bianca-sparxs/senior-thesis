from __future__ import annotations

from typing import TYPE_CHECKING

import colors

if TYPE_CHECKING:
    from tcod import Console

def render_bar(
    console: Console, current_value: int, maximum_value: int, total_width: int
) -> None:
    bar_width = int(float(current_value) / maximum_value * total_width)

    console.draw_rect(x=1, y=30, width=15, height=1, ch=1, bg=colors.bar_empty)

    if bar_width > 0:
        console.draw_rect(
            x=1, y=30, width=bar_width, height=1, ch=1, bg=colors.bar_filled
        )

    console.print(
        x=2, y=30, string=f"HP: {current_value}/{maximum_value}", fg=colors.bar_text
    )

def render_task(
    console: Console, motivation: int, T_energy: int, special: bool
) -> None:

    console.draw_rect(x=1, y=1, width=33, height=9, ch=3, bg=colors.bar_filled)


    console.print(
        x=2, y=2, string=f"""motivation: {motivation}\nT energy gain: {T_energy}\nspecial?: {special}\n
        \n[y]- accept task\n[n]- move onwards""", fg=colors.bar_text
    )