import pandas as pd


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    df = pd.DataFrame(np.sqrt(np.square(df.values[:, np.newaxis] - df.values).sum(axis=2)),columns=df.index, index=df.index)
    return df


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    df = df.unstack().reset_index(name='distance')
    df.columns = ['id_start', 'id_end', 'distance']
    return df


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here
    reference_df = df[df['id_start'] == reference_id]

    # Check if the reference_df is empty
    if reference_df.empty:
        print(f"No data found for reference value {reference_id}")
        return []

    # Check if there are non-zero distances in the reference_df
    if (reference_df['distance'] == 0).all():
        print("All distances are zero in the reference_df.")
        return []

    # Calculating average distance for the reference value
    average_distance = reference_df['distance'].mean()

    # Print the average_distance for debugging
    print(f"Average Distance for {reference_id}: {average_distance}")

    # Define the threshold range
    threshold_lower = 0.9 * average_distance
    threshold_upper = 1.1 * average_distance

    # Filter the DataFrame based on the threshold range
    filtered_df = df[(df['id_start'] != reference_id) & (df['distance'] >= threshold_lower) & (df['distance'] <= threshold_upper)]

    print("Filtered DataFrame:")
    print(filtered_df)

    result_ids = sorted(filtered_df['id_start'].unique())

    return result_ids


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    # Calculate toll rates for each vehicle type
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        df[vehicle_type] = df['distance'] * rate_coefficient
    return df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    time_intervals = {
        (0, 6): 0.1,
        (6, 12): 0.2,
        (12, 18): 0.3,
        (18, 24): 0.4
    }
    def get_time_based_rate(timestamp):
        hour = timestamp.hour
        for interval, rate in time_intervals.items():
            if interval[0] <= hour < interval[1]:
                return rate
        return 0  # Default rate if not found in any interval

    df['time_based_toll_rate'] = df['timestamp'].apply(get_time_based_rate)

    return df
