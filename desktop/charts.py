from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

def create_equipment_chart(distribution):
    """
    distribution: dict like {"Pump": 4, "Valve": 3, ...}
    """
    fig = Figure(figsize=(5, 4))
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)

    labels = list(distribution.keys())
    values = list(distribution.values())

    ax.bar(labels, values)
    ax.set_title("Equipment Type Distribution")
    ax.set_xlabel("Equipment Type")
    ax.set_ylabel("Count")

    ax.tick_params(axis='x', rotation=45)

    fig.tight_layout()
    return canvas
