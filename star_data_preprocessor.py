import numpy as np
import pandas as pd

def periodic_shift(value: float, period: float) -> float:
    return ((value + period / 2 + period) % period) - (period / 2)

def center_transit_in_the_curve(points: list[tuple[float, float]], period_in_hours: float) -> list[tuple[float, float]]:
    new_points = list(map(lambda x: (periodic_shift(x[0], period_in_hours), x[1]), points))
    new_points.sort(key=lambda x: x[0])
    return new_points

def bin_points(points: list[tuple[float, float]], bin_width: float = 0.1) -> list[tuple[float, float]]:

    if not points:
        return []

    df = pd.DataFrame(points, columns=["T", "Flux"])
    min_t = df["T"].min()
    max_t = df["T"].max()
    bins = pd.interval_range(start=min_t, end=(max_t + bin_width), freq=bin_width, closed='left')

    df["T_bin"] = pd.cut(df["T"], bins)

    binned_df = df.groupby("T_bin", observed=True).agg({
        "T": "mean",
        "Flux": "mean"
    }).dropna()

    binned_points = list(binned_df.itertuples(index=False, name=None))

    return binned_points


def custom_binning_with_in_transit_priority(
    points: list[tuple[float, float]], t14_in_days,
    num_in_transit_bins=51, num_out_of_transit_bins=90
) -> list[tuple[float, float]]:
    """
    Bin the phase-folded light curve, giving higher resolution to the in-transit region.
    Assumes transit is centered at 0.

    Args:
        points (list[tuple[float, float]]): Light curve, list of pairs of time and flux at an instance.
        t14_in_hours (float): Transit duration (T₁₄) in hours.
        num_in_transit_bins (int): Number of bins to create in the in-transit region.
        num_out_of_transit_bins (int): Number of bins to create in the out-of-transit region.

    Returns:
        list[tuple[float, float]]: Binned phases and corresponding binned flux values.
    """
    
    t14_in_hours = t14_in_days * 24
    in_transit_min = -t14_in_hours / 2
    in_transit_max = t14_in_hours / 2
    
    x, y = zip(*points)
    
    phase = np.array(x)
    flux = np.array(y)

    # Mask in-transit and out-of-transit points
    in_transit_mask = (phase >= in_transit_min) & (phase <= in_transit_max)
    out_transit_mask = ~in_transit_mask

    # In-transit binning (fine)
    in_bins = np.linspace(in_transit_min, in_transit_max, num_in_transit_bins + 1)
    in_digitized = np.digitize(phase[in_transit_mask], in_bins)
    in_binned_flux = [flux[in_transit_mask][in_digitized == i].mean() if np.any(in_digitized == i) else np.nan
                      for i in range(1, len(in_bins))]
    in_bin_centers = (in_bins[:-1] + in_bins[1:]) / 2

    # Out-of-transit binning (coarse), over the remaining phase range
    phase_min = np.min(phase)
    phase_max = np.max(phase)
    out_bins = np.linspace(phase_min, phase_max, num_out_of_transit_bins + 1)
    # Remove bins that overlap with in-transit region
    out_bins = out_bins[(out_bins < in_transit_min) | (out_bins > in_transit_max)]
    out_digitized = np.digitize(phase[out_transit_mask], out_bins)
    out_binned_flux = [flux[out_transit_mask][out_digitized == i].mean() if np.any(out_digitized == i) else np.nan
                       for i in range(1, len(out_bins))]
    out_bin_centers = (out_bins[:-1] + out_bins[1:]) / 2

    # Combine and sort
    all_bin_centers = np.concatenate([out_bin_centers, in_bin_centers])
    all_binned_flux = np.concatenate([out_binned_flux, in_binned_flux])

    valid_mask = ~np.isnan(all_binned_flux)
    sorted_indices = np.argsort(all_bin_centers[valid_mask])
    
    binned_points = list(zip(all_bin_centers[valid_mask][sorted_indices], all_binned_flux[valid_mask][sorted_indices]))

    return binned_points