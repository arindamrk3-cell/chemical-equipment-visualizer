from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


def create_equipment_chart(distribution):
    fig = Figure(figsize=(6, 4))
    canvas = FigureCanvas(fig)

    ax = fig.add_subplot(111)

    labels = list(distribution.keys())
    values = list(distribution.values())

    ax.bar(labels, values, color="#60a5fa")

    ax.set_title("Equipment Type Distribution")
    ax.set_xlabel("Equipment Type")
    ax.set_ylabel("Count")

    ax.tick_params(axis="x", rotation=45)

    # DARK MODE COLORS
    ax.set_facecolor("#1f1f1f")
    fig.patch.set_facecolor("#1f1f1f")

    ax.title.set_color("white")
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.tick_params(colors="white")

    fig.tight_layout()
    return canvas
