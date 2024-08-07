from scilightcon.plot import apply_style, reset_style, add_watermark, add_watermarks
import pytest
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

@pytest.mark.skip(reason="helper")
def plot_something(n, figure_name):
    fig = plt.figure(figure_name)

    for i in np.arange(n):
        ax = fig.add_subplot(1, n, i+1)
        ax.plot([1,2,3])

def test_apply_style():
    apply_style()

    plot_something(1, "test")

def test_reset_style():
    reset_style()


def test_watermark():
    apply_style()

    plot_something(1, "test watermark")

    add_watermark(plt.gcf())

    plt.show()

def test_watermarks():
    apply_style()

    plot_something(4, "test watermarks")

    add_watermarks(plt.gcf())

    plt.show()