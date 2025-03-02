""" Periods with Ignore
This program helps you find available time slots within a given period, by
automatically excluding a specific time range that repeats every day
(the "ignore range").  Think of it like scheduling something, but you want to
avoid certain hours each day.
"""

from datetime import datetime, timedelta, time

def get_valid_ranges(period, ignore_range):
    """
    Calculates valid timestamp ranges within a given period, excluding a recurring daily ignore range.

    Args:
        period: A list of two strings representing the start and end timestamps of the period
                (e.g., ['2024-08-12 09:00', '2024-08-15 17:00']).
        ignore_range: A list of two strings representing the start and end times of the daily ignore range
                      (e.g., ['01:00', '06:00']).  This range is assumed to be less than 24 hours.

    Returns:
        A list of tuples, where each tuple is a valid timestamp range (start_timestamp, end_timestamp)
        as strings formatted as 'YYYY-MM-DD HH:MM'. These ranges are within the given period and outside
        the daily ignore range, and are designed to be sequential and exhaustively cover the valid time
        within the period.
    """
    # Extract start and end strings for period and ignore range
    period_start_str, period_end_str = period
    ignore_start_time_str, ignore_end_time_str = ignore_range

    # Convert period strings to datetime objects
    period_start = datetime.strptime(period_start_str, "%Y-%m-%d %H:%M")
    period_end = datetime.strptime(period_end_str, "%Y-%m-%d %H:%M")
    # Convert ignore range time strings to time objects
    ignore_start_time = time.fromisoformat(ignore_start_time_str)
    ignore_end_time = time.fromisoformat(ignore_end_time_str)

    valid_ranges = []  # Initialize an empty list to store valid time ranges
    current_time = period_start  # Start processing from the beginning of the period

    while (
        current_time < period_end
    ):  # Iterate as long as the current time is before the period end
        current_date = (
            current_time.date()
        )  # Get the date of the current time for daily ignore range calculation
        ignore_start_datetime = datetime.combine(
            current_date, ignore_start_time
        )  # Combine date with ignore start time
        ignore_end_datetime = datetime.combine(
            current_date, ignore_end_time
        )  # Combine date with ignore end time

        if current_time < ignore_start_datetime:
            # Case 1: Current time is before the daily ignore period starts.
            # Valid range extends from current time up to the start of the ignore period (or period end).
            valid_end_time = min(
                ignore_start_datetime, period_end
            )  # End of valid range is either ignore start or period end
            if (
                current_time < valid_end_time
            ):  # Ensure start is before end to have a valid range
                valid_ranges.append(
                    (
                        current_time.strftime("%Y-%m-%d %H:%M"),
                        valid_end_time.strftime("%Y-%m-%d %H:%M"),
                    )
                )
                current_time = (
                    valid_end_time  # Move current time to the end of the valid range
                )
            else:
                current_time = ignore_start_datetime  # If no valid range, move to ignore start to avoid infinite loop

        elif ignore_start_datetime <= current_time < ignore_end_datetime:
            # Case 2: Current time is within the daily ignore period.
            # Skip the ignore period by setting current time to the end of the ignore period.
            current_time = ignore_end_datetime

        elif ignore_end_datetime <= current_time:
            # Case 3: Current time is after the daily ignore period ends.
            # Valid range extends from current time up to the next day's ignore start or period end.
            valid_end_time = period_end  # Initially assume valid until period end
            next_day_date = current_date + timedelta(
                days=1
            )  # Calculate next day's date
            next_day_ignore_start_datetime = datetime.combine(
                next_day_date, ignore_start_time
            )  # Next day's ignore start

            # Determine the valid end time: either period end or next day's ignore start (whichever is earlier and within period)
            if (
                current_time < next_day_ignore_start_datetime
                and next_day_ignore_start_datetime <= period_end
            ):
                valid_end_time = next_day_ignore_start_datetime  # End at next day's ignore start if it's within the period
            # else if current_time >= next_day_ignore_start_datetime, or next_day_ignore_start_datetime > period_end,
            # then valid_end_time remains period_end (or potentially already set to period_end initially).

            if (
                current_time < valid_end_time
            ):  # Ensure start is before end for a valid range
                valid_ranges.append(
                    (
                        current_time.strftime("%Y-%m-%d %H:%M"),
                        valid_end_time.strftime("%Y-%m-%d %H:%M"),
                    )
                )
                current_time = (
                    valid_end_time  # Move current time to the end of the valid range
                )
            else:
                current_time = valid_end_time  # If no valid range, move to valid_end_time to avoid infinite loop

        else:
            break  # Safety break to prevent infinite loop in unexpected scenarios

    return valid_ranges  # Return the list of valid time ranges


def print_valid_ranges_formatted(valid_ranges):
    """
    Prints the valid timestamp ranges in a user-friendly format.

    Args:
        valid_ranges: A list of tuples, where each tuple is a valid timestamp range
                      (start_timestamp, end_timestamp) as strings.
    """
    if not valid_ranges:
        print(
            "No valid ranges found within the given period and outside the ignore range."
        )
        return

    print("Valid Time Ranges:")
    for index, time_range in enumerate(
        valid_ranges, 1
    ):  # Enumerate to number the ranges starting from 1
        start_time, end_time = time_range
        print(f"Range {index}:")
        print(f"  Start: {start_time}")
        print(f"  End:   {end_time}")
        if index < len(valid_ranges):  # Add a separator if it's not the last range
            print("-" * 15)  # Separator line for better readability



print("\n#################  Test Case 1  #################")
period = ["2024-01-01 10:00", "2024-01-02 23:00"]
ignore_range = ["02:00", "05:00"]
print(f"Period: {period}")
print(f"Ignore Range: {ignore_range}")
print_valid_ranges_formatted(get_valid_ranges(period, ignore_range))

print("\n#################  Test Case 2  #################")
period = ["2024-01-01 10:00", "2024-01-05 17:00"]
ignore_range = ["02:00", "06:00"]
print(f"Period: {period}")
print(f"Ignore Range: {ignore_range}")
print_valid_ranges_formatted(get_valid_ranges(period, ignore_range))

print("\n#################  Test Case 3  #################")
period = ["2024-01-01 10:00", "2024-01-01 23:00"]
ignore_range = ["05:00", "19:00"]
print(f"Period: {period}")
print(f"Ignore Range: {ignore_range}")
print_valid_ranges_formatted(get_valid_ranges(period, ignore_range))

# # Define the ignore range for all test cases
# common_ignore_range = ["01:00", "06:00"]

# # Test cases based on user examples:

# print("\n#################  Test Case 1: Multiple periods  #################")
# print("Period: ['2024-08-12 09:00', '2024-08-15 17:00']")
# print("Ignore Range: ['01:00', '06:00']")
# print_valid_ranges_formatted(
#     get_valid_ranges(["2024-08-12 09:00", "2024-08-15 17:00"], common_ignore_range)
# )

# print("\n#################  Test Case 2: No Periods #################")
# print("Period: ['2024-08-12 01:00', '2024-08-12 06:00']")
# print("Ignore Range: ['01:00', '06:00']")
# print_valid_ranges_formatted(
#     get_valid_ranges(["2024-08-12 01:00", "2024-08-12 06:00"], common_ignore_range)
# )

# print("\n#################  Test Case 3: Only middle and End periods #################")
# print("Period: ['2024-08-12 01:00', '2024-08-13 17:00']")
# print("Ignore Range: ['01:00', '06:00']")
# print_valid_ranges_formatted(
#     get_valid_ranges(["2024-08-12 01:00", "2024-08-13 17:00"], common_ignore_range)
# )

# print("\n#################  Test Case 4: Only middle periods #################")
# print("Period: ['2024-08-12 01:00', '2024-08-13 01:00']")
# print("Ignore Range: ['01:00', '06:00']")
# print_valid_ranges_formatted(
#     get_valid_ranges(["2024-08-12 01:00", "2024-08-13 01:00"], common_ignore_range)
# )

# print(
#     "\n#################  Test Case 5: No middle periods, only start and end #################"
# )
# print("Period: ['2024-08-12 04:00', '2024-08-12 07:00']")
# print("Ignore Range: ['01:00', '06:00']")
# print_valid_ranges_formatted(
#     get_valid_ranges(["2024-08-12 04:00", "2024-08-12 07:00"], common_ignore_range)
# )

# print(
#     "\n#################  Test Case 6: Period within single day, outside ignore range #################"
# )
# print("Period: ['2024-08-15 09:00', '2024-08-15 17:00']")
# print("Ignore Range: ['01:00', '06:00']")
# print_valid_ranges_formatted(
#     get_valid_ranges(["2024-08-15 09:00", "2024-08-15 17:00"], common_ignore_range)
# )

# print(
#     "\n#################  Test Case 7: Period overlaps start of ignore range #################"
# )
# print("Period: ['2024-08-15 00:00', '2024-08-15 02:00']")
# print("Ignore Range: ['01:00', '06:00']")
# print_valid_ranges_formatted(
#     get_valid_ranges(["2024-08-15 00:00", "2024-08-15 02:00"], common_ignore_range)
# )

# print(
#     "\n#################  Test Case 8: Period overlaps end of ignore range #################"
# )
# print("Period: ['2024-08-15 05:30', '2024-08-15 07:00']")
# print("Ignore Range: ['01:00', '06:00']")
# print_valid_ranges_formatted(
#     get_valid_ranges(["2024-08-15 05:30", "2024-08-15 07:00"], common_ignore_range)
# )

# print(
#     "\n#################  Test Case 9: Period fully within ignore range #################"
# )
# print("Period: ['2024-08-15 03:00', '2024-08-15 05:00']")
# print("Ignore Range: ['01:00', '06:00']")
# print_valid_ranges_formatted(
#     get_valid_ranges(["2024-08-15 03:00", "2024-08-15 05:00"], common_ignore_range)
# )

# print(
#     "\n#################  Test Case 10: Period spans over 24 hrs, crossing ignore periods #################"
# )
# print("Period: ['2024-08-15 00:00', '2024-08-16 00:00']")
# print("Ignore Range: ['01:00', '06:00']")
# print_valid_ranges_formatted(
#     get_valid_ranges(["2024-08-15 00:00", "2024-08-16 00:00"], common_ignore_range)
# )
