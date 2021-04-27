from __future__ import annotations

from typing import TYPE_CHECKING

import colors

if TYPE_CHECKING:
    from tcod import Console

def render_bar(
    console: Console, current_value: int, maximum_value: int, total_width: int
) -> None:
    bar_width = int(float(current_value) / maximum_value * total_width)

    console.draw_rect(x=0, y=45, width=33, height=1, ch=1, bg=colors.bar_empty)

    if bar_width > 0:
        console.draw_rect(
            x=0, y=45, width=bar_width, height=1, ch=1, bg=colors.bar_filled
        )

    console.print(
        x=1, y=45, string=f"HP: {current_value}/{maximum_value}", fg=colors.bar_text
    )

def render_task(
    console: Console, motivation: int, T_energy: int, special: bool
) -> None:

    console.draw_rect(x=80, y=45, width=33, height=40, ch=3, bg=colors.bar_empty)


    console.print(
        x=1, y=45, string=f"motivation: {motivation}\nT energy gain: {T_energy}\nspecial: {special}", fg=colors.bar_text
    )