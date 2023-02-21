# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 19:03:22 2019

@author: Lucas Carter
"""
from typing import Optional

import numpy as np
import matplotlib.pyplot as plt

#### Credit to Kalman and Bayesian Filtering in Python by R. Labbe
#### for set_labels. These utilities helped save
#### time in plotting filter performance


def set_labels(
    ax: plt.Axes,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
) -> None:
    """For axis ax, add labels for x-axis, y-axis, or title if provided."""
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title)


def plot_residual_error(
    residual: np.array, dt: float = 1.0, ax: Optional[plt.Axes] = None
) -> plt.Axes:
    """Plot filter residual error.

    Parameters
    ----------
    residual : np.array
        Array of residual error values.
    dt : float, optional
        Time step between values. Used to create a time array starting
        at zero. Defaults to 1.
    ax : Optional[plt.Axes], optional
        Axis to plot values. One is created if not provided.
    Returns
    -------
    plt.Axes
        Formatted plot.
    """

    if not isinstance(residual, np.ndarray):
        residual = np.asarray(residual)

    if ax is None:
        _, ax = plt.subplots()

    time = np.arange(0, residual.size * dt, dt)
    ax.plot(time, residual, linewidth=2)

    set_labels(
        ax=ax,
        xlabel="Time (seconds)",
        ylabel="Residual Error",
        title="Residual Error over Time",
    )
    ax.grid()

    return ax


def plot_squared_residual_error(
    residual: np.ndarray, dt: float = 1.0, ax: Optional[plt.Axes] = None
) -> plt.Axes:
    """Plot squared residual error of filter over time.

    Parameters
    ----------
    residual : np.array
        Array of residual error values.
    dt : float, optional
        Time step between values. Used to create a time array starting
        at zero. Defaults to 1.
    ax : Optional[plt.Axes], optional
        Axis to plot values. One is created if not provided.
    Returns
    -------
    plt.Axes
        Formatted plot.
    """

    squared_residual = np.power(residual, 2)

    ax = plot_residual_error(squared_residual, dt, ax)

    set_labels(
        ax,
        title="Squared Residual Error vs Time",
        xlabel="Time (seconds)",
        ylabel="Squared Residual Error",
    )
    ax.grid()

    return ax


def plot_probs(probs, dt=1, ax=plt):
    t = np.arange(0, len(probs) * dt, dt)
    ax.plot(t, probs, linewidth=3)

