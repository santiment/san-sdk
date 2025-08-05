"""
Change calculation functions for time series analysis.

This module provides pandas-based implementations for calculating various types
of percentage changes in time series data, including:
- N-day/N-period changes
- Moving average calculations
- Change calculations with proper NaN and zero handling

All functions handle edge cases properly:
- NaN values (both old and new)
- Zero values (division by zero)
- Boundary conditions
- Missing data
"""

import pandas as pd
import numpy as np
from typing import Union, Optional


def compute_nd_change(series: pd.Series, days: int = 1) -> pd.Series:
    """
    Compute the n-day percentage change for a pandas Series.

    This function calculates the percentage change between the current value
    and the value n periods ago, with proper handling of edge cases.

    Args:
        series: pandas Series with numeric values
        days: number of periods to look back (default: 1)

    Returns:
        pandas Series with percentage changes

    Examples:
        >>> data = pd.Series([100, 110, 99, 108])
        >>> changes = compute_nd_change(data, days=1)
        >>> print(changes)
        0       NaN
        1      0.10
        2     -0.10
        3      0.09
    """

    old_value = series.shift(days)
    value = series

    # Handle different cases
    result = pd.Series(index=series.index, dtype=float)

    # Both NaN -> NaN
    both_nan = pd.isna(value) | pd.isna(old_value)
    result[both_nan] = np.nan

    # Both zero -> 0% change
    both_zero = (old_value == 0) & (value == 0) & ~both_nan
    result[both_zero] = 0

    # Old value is zero, new value is not -> 100% increase
    old_zero_new_nonzero = (old_value == 0) & (value != 0) & ~both_nan
    result[old_zero_new_nonzero] = 1

    # Normal case: calculate percentage change
    normal_case = ~both_nan & ~both_zero & ~old_zero_new_nonzero
    result[normal_case] = (value[normal_case] / old_value[normal_case]) - 1

    return result


def compute_nd_change_vectorized(series: pd.Series, days: int = 1) -> pd.Series:
    """
    Vectorized version of compute_nd_change for better performance.

    Args:
        series: pandas Series with numeric values
        days: number of periods to look back

    Returns:
        pandas Series with percentage changes
    """

    old_value = series.shift(days)
    value = series

    # Vectorized conditions using pandas operations
    both_nan = pd.isna(value) | pd.isna(old_value)
    both_zero = (old_value == 0) & (value == 0)
    old_zero_new_nonzero = (old_value == 0) & (value != 0)
    normal_case = ~both_nan & ~both_zero & ~old_zero_new_nonzero

    result = pd.Series(index=series.index, dtype=float)
    result[both_nan] = np.nan
    result[both_zero] = 0
    result[old_zero_new_nonzero] = 1
    result[normal_case] = (value[normal_case] / old_value[normal_case]) - 1

    return result


def compute_1d_change(series: pd.Series) -> pd.Series:
    """
    Compute 1-day (1-period) percentage change.

    Args:
        series: pandas Series with numeric values

    Returns:
        pandas Series with 1-day percentage changes
    """
    return compute_nd_change_vectorized(series, days=1)


def compute_7d_change(series: pd.Series) -> pd.Series:
    """
    Compute 7-day (7-period) percentage change.

    Args:
        series: pandas Series with numeric values

    Returns:
        pandas Series with 7-day percentage changes
    """
    return compute_nd_change_vectorized(series, days=7)


def compute_30d_change(series: pd.Series) -> pd.Series:
    """
    Compute 30-day (30-period) percentage change.

    Args:
        series: pandas Series with numeric values

    Returns:
        pandas Series with 30-day percentage changes
    """
    return compute_nd_change_vectorized(series, days=30)


# Moving average functions
def compute_moving_average(
    series: pd.Series, hours: int, min_periods: int = None
) -> pd.Series:
    """
    Calculate moving average for an arbitrary period in hours.

    This function uses pandas' time-aware rolling windows to compute moving averages
    based on actual time periods rather than just the number of observations.

    Args:
        series: pandas Series with DatetimeIndex and numeric values
        hours: number of hours for the moving average window
        min_periods: minimum number of observations in window required to have a value
                    (defaults to 1)

    Returns:
        pandas Series with moving average values

    Examples:
        >>> import pandas as pd
        >>> dates = pd.date_range('2024-01-01', periods=100, freq='H')
        >>> data = pd.Series(range(100), index=dates)
        >>> ma_24h = compute_moving_average(data, hours=24)
        >>> ma_7d = compute_moving_average(data, hours=168)  # 7*24 hours
    """

    if min_periods is None:
        min_periods = 1

    # Use time-based rolling window
    window = pd.Timedelta(hours=hours)
    return series.rolling(window=window, min_periods=min_periods).mean()


def compute_moving_average_change(
    series: pd.Series, hours: int, change_period_hours: int = 24
) -> pd.Series:
    """
    Calculate the percentage change of a moving average over a specified period.

    This function first computes a moving average, then calculates the percentage
    change of that moving average over the specified change period.

    Args:
        series: pandas Series with DatetimeIndex and numeric values
        hours: hours for the moving average calculation
        change_period_hours: hours for the change calculation (default: 24)

    Returns:
        pandas Series with moving average percentage changes

    Example:
        >>> # 24-hour moving average, then 24-hour change of that MA
        >>> ma_change = compute_moving_average_change(data, hours=24, change_period_hours=24)
    """

    # First compute the moving average
    ma = compute_moving_average(series, hours)

    # Then compute the change - use frequency-aware shift
    if hasattr(ma.index, "freq") and ma.index.freq is not None:
        # If we have a regular frequency, calculate periods needed
        freq_seconds = ma.index.freq.delta.total_seconds()
        periods = int(change_period_hours * 3600 / freq_seconds)
        old_ma = ma.shift(periods)
    else:
        # Use time-based shift for irregular frequencies
        time_shift = pd.Timedelta(hours=change_period_hours)
        old_ma = ma.shift(freq=time_shift)

    # Apply the same change calculation logic
    both_nan = pd.isna(ma) | pd.isna(old_ma)
    both_zero = (old_ma == 0) & (ma == 0)
    old_zero_new_nonzero = (old_ma == 0) & (ma != 0)
    normal_case = ~both_nan & ~both_zero & ~old_zero_new_nonzero

    result = pd.Series(index=ma.index, dtype=float)
    result[both_nan] = np.nan
    result[both_zero] = 0
    result[old_zero_new_nonzero] = 1
    result[normal_case] = (ma[normal_case] / old_ma[normal_case]) - 1

    return result


def compute_nd_change_numpy(values: np.ndarray, n_periods: int = 1) -> np.ndarray:
    """
    Compute the n-period change metric using pure numpy operations.

    This function replicates the logic from social_change_metrics.py using
    vectorized numpy operations for maximum performance.

    Args:
        values: numpy array of numeric values
        n_periods: number of periods to look back for comparison (default: 1)

    Returns:
        numpy array with n-period change values

    Examples:
        >>> values = np.array([100, 110, 99, 108, 115])
        >>> changes = compute_nd_change_numpy(values, n_periods=1)
        >>> print(changes)
        [nan 0.1 -0.1 0.090909 0.064815]
    """

    if len(values) == 0:
        return np.array([])

    # Ensure float type for NaN handling
    current_values = values.astype(float)

    # Handle case where n_periods >= length of data
    if n_periods >= len(current_values):
        return np.full_like(current_values, np.nan)

    # Create shifted arrays
    old_values = np.full_like(current_values, np.nan)
    old_values[n_periods:] = current_values[:-n_periods]

    # Initialize result array
    result = np.full_like(current_values, np.nan)

    # Create boolean masks for different conditions
    both_nan = np.isnan(current_values) | np.isnan(old_values)
    both_zero = (old_values == 0) & (current_values == 0) & ~both_nan
    old_zero_new_nonzero = (old_values == 0) & (current_values != 0) & ~both_nan
    normal_case = ~both_nan & ~both_zero & ~old_zero_new_nonzero & (old_values != 0)

    # Apply conditions using numpy.where and boolean indexing
    result[both_nan] = np.nan
    result[both_zero] = 0.0
    result[old_zero_new_nonzero] = 1.0
    with np.errstate(divide="ignore", invalid="ignore"):
        result[normal_case] = (
            current_values[normal_case] / old_values[normal_case]
        ) - 1.0

    return result

