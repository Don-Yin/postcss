"""Compare measured Warning.toString() start positions before and after the fix."""

from __future__ import annotations

import json
from pathlib import Path

from python_plotting_convention import (
    FULL_TEXT_WIDTH_CM,
    publication_subplots,
    tag_artist,
)


def build_figure(*, target_width_cm: float = FULL_TEXT_WIDTH_CM):
    directory = Path(__file__).resolve().parent
    base = json.loads((directory / "base-results.json").read_text())
    fixed = json.loads((directory / "fixed-results.json").read_text())
    if len(base["cases"]) != len(fixed["cases"]):
        raise ValueError("Measurements must describe matching cases")

    figure, axes = publication_subplots(
        1,
        len(base["cases"]),
        target_width_cm=target_width_cm,
        height_cm=8.6,
        sharex=True,
        sharey=True,
    )
    handles = []
    for ax, before, after in zip(axes, base["cases"], fixed["cases"], strict=True):
        requested = before["requested"]
        if requested != after["requested"] or before["css"] != after["css"]:
            raise ValueError("Measurements must use the same CSS and start")
        if before["properties"] != requested or after["properties"] != requested:
            raise ValueError("Warning properties must preserve the requested start")
        requested_mark, = ax.plot(
            requested["column"],
            requested["line"],
            marker="o",
            markersize=15,
            markerfacecolor="none",
            markeredgecolor="#303030",
            markeredgewidth=1.2,
            linestyle="none",
            label="Requested",
        )
        before_mark, = ax.plot(
            before["formatted"]["column"],
            before["formatted"]["line"],
            marker="x",
            markersize=10,
            markeredgewidth=2,
            color="#bf5b17",
            linestyle="none",
            label="Before toString()",
        )
        after_mark, = ax.plot(
            after["formatted"]["column"],
            after["formatted"]["line"],
            marker="+",
            markersize=10,
            markeredgewidth=2,
            color="#1764a0",
            linestyle="none",
            label="After toString()",
        )
        handles = [requested_mark, before_mark, after_mark]
        ax.set_title(
            f'{before["name"]} ({requested["line"]}:{requested["column"]})',
            loc="left",
            fontsize=11,
        )
        ax.set_xlim(0.6, 3.4)
        ax.set_ylim(2.4, 0.6)
        ax.set_xticks([1, 2, 3])
        ax.set_yticks([1, 2])
        ax.set_box_aspect(1)
        ax.grid(linestyle=":", alpha=0.35)
        ax.set_axisbelow(True)

    axes[0].set_ylabel("Line")
    tag_artist(axes[0], semantic_role="body")
    figure.supxlabel("Column", y=0.02)
    figure.legend(
        handles=handles,
        loc="upper center",
        bbox_to_anchor=(0.52, 0.995),
        ncol=3,
        fontsize=10,
        frameon=False,
        handletextpad=0.5,
        columnspacing=1.4,
    )
    figure.subplots_adjust(left=0.10, right=0.98, bottom=0.17, top=0.83, wspace=0.25)
    return figure, {
        "scientific_job": "comparison",
        "data_sources": ["base-results.json", "fixed-results.json"],
        "base_revision": base["revision"],
        "fixed_revision": fixed["revision"],
        "encoding": "The plus lies inside the requested-position ring after the fix.",
    }
