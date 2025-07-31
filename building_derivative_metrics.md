# Building Derivative Metrics: A Practical Guide

This document demonstrates how to build derivative metrics from base time series data using the change calculation and moving average functions. We'll show how to transform a single base metric into multiple derived metrics that provide different analytical perspectives.

## Overview

**Derivative metrics** are computed metrics that are derived from existing base metrics through mathematical transformations. They provide additional insights and analytical value beyond the raw data.

## Base Metric

For this example, we'll use:
- **Base Metric**: `social_dominance_total` - A time series representing social media dominance

## Target Derivative Metrics

From this base metric, we'll create the following derivatives:

1. **`social_dominance_total_change_1d`** - 1-day percentage change
2. **`social_dominance_total_24h_moving_average`** - 24-hour moving average  
3. **`social_dominance_total_24h_moving_average_change_1d`** - 1-day change of the 24-hour moving average

We're using this set of metric as an example, because the rest of the metrics can be calculated with the same functions, but different parameter for days in hours in correspondent functions.

## Functions Used

- `compute_nd_change()` - Standard change calculation
- `compute_nd_change_vectorized()` - Optimized vectorized change calculation
- `compute_nd_change_numpy()` - Pure numpy implementation for maximum performance
- `compute_moving_average()` - Time-aware moving average calculation

## Prerequisites

Before running the examples, ensure you have the required dependencies installed:

```bash
pip install pandas numpy sanpy python-dotenv
```

You'll also need access to the Santiment API. You can get your API key from [Santiment](https://app.santiment.net/) and set it up according to the [sanpy documentation](https://github.com/santiment/sanpy).

## Implementation

### Step 1: Data Preparation

```python
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
import san
from change_functions import compute_nd_change, compute_nd_change_vectorized, compute_nd_change_numpy, compute_moving_average

# Load your time series data using Santiment API
load_dotenv()

san.ApiConfig.api_key = os.getenv("SAN_API_KEY")

data = san.get(
    "social_dominance_total",
    slug="bitcoin",
    from_date="2024-01-01",
    to_date="2025-07-01",
    interval="1d"
)

# The data comes with datetime index already set
# Extract the base metric
social_dominance_total = data['value']

```

### Step 2: Building Derivative Metric #1 - 1-Day Change

The first derivative metric calculates the 1-day percentage change of the base metric.

```python
# Method 1: Using standard implementation
social_dominance_total_change_1d_v1 = compute_nd_change(social_dominance_total, days=1)

# Method 2: Using vectorized implementation (recommended for better performance)
social_dominance_total_change_1d_v2 = compute_nd_change_vectorized(social_dominance_total, days=1)

# Method 3: Using pure numpy implementation (best for very large datasets)
social_dominance_total_change_1d_v3 = compute_nd_change_numpy(social_dominance_total.values, n_periods=1)

# Convert back to pandas Series for consistency
social_dominance_total_change_1d_v3 = pd.Series(
    social_dominance_total_change_1d_v3, 
    index=social_dominance_total.index,
    name='social_dominance_total_change_1d'
)

# Verify all methods produce identical results
print("Results comparison:")
print(f"Max difference v1 vs v2: {np.nanmax(np.abs(social_dominance_total_change_1d_v1 - social_dominance_total_change_1d_v2))}")
print(f"Max difference v2 vs v3: {np.nanmax(np.abs(social_dominance_total_change_1d_v2 - social_dominance_total_change_1d_v3))}")


```

### Step 3: Building Derivative Metric #2 - 24-Hour Moving Average

The second derivative metric smooths the base metric using a 24-hour rolling window.

```python
# Calculate 24-hour moving average
social_dominance_total_24h_moving_average = compute_moving_average(
    social_dominance_total, 
    hours=24,
    min_periods=1  # Allow calculation even with fewer than 24 data points
)


```

### Step 4: Building Derivative Metric #3 - Change of Moving Average

The third derivative metric calculates the 1-day percentage change of the moving average.

```python
# Calculate 1-day change of the 24-hour moving average
# Method 1: Using vectorized pandas implementation
social_dominance_total_24h_moving_average_change_1d_v1 = compute_nd_change_vectorized(
    social_dominance_total_24h_moving_average, 
    days=1
)

# Method 2: Using numpy implementation for better performance
social_dominance_total_24h_moving_average_change_1d_v2 = compute_nd_change_numpy(
    social_dominance_total_24h_moving_average.values, 
    n_periods=1
)
# Convert back to pandas Series
social_dominance_total_24h_moving_average_change_1d_v2 = pd.Series(
    social_dominance_total_24h_moving_average_change_1d_v2,
    index=social_dominance_total_24h_moving_average.index,
    name='social_dominance_total_24h_moving_average_change_1d'
)

```

## Performance Considerations

### When to Use Each Implementation

1. **`compute_nd_change()`** - Standard implementation
   - ✅ Use for: Small to medium datasets (<10K rows)
   - ✅ Use for: Development and prototyping
   - ❌ Avoid for: Very large datasets

2. **`compute_nd_change_vectorized()`** - Vectorized pandas implementation  
   - ✅ Use for: Most production scenarios
   - ✅ Use for: Medium to large datasets (10K-1M rows)
   - ✅ Use for: When you need pandas integration

3. **`compute_nd_change_numpy()`** - Pure numpy implementation
   - ✅ Use for: Very large datasets (>1M rows)
   - ✅ Use for: Performance-critical applications
   - ✅ Use for: Memory-constrained environments
   - ❌ Avoid for: When you need pandas features (indexing, etc.)

