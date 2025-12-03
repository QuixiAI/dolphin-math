import random
from base_generator import ProblemGenerator
from helpers import step, jid


class MeanGenerator(ProblemGenerator):
    """
    Generates mean (average) calculation problems.

    Formula: Mean = Sum of values / Number of values

    Op-codes used:
    - STAT_SETUP: Set up the dataset (values)
    - STAT_SUM: Calculate sum (calculation, result)
    - STAT_COUNT: Count values (count)
    - STAT_DIVIDE: Divide sum by count (calculation, result)
    - Z: Final answer
    """

    def __init__(self, dataset_size: int = None):
        """
        Initialize generator.

        Args:
            dataset_size: Number of values in dataset (5-10 if None)
        """
        self.dataset_size = dataset_size

    def generate(self) -> dict:
        """Generate a mean calculation problem."""
        size = self.dataset_size or random.randint(5, 10)

        # Generate values that give a clean mean
        mean_target = random.randint(30, 70)
        total = mean_target * size

        # Distribute total among values, ensuring all positive
        values = []
        remaining = total
        for i in range(size - 1):
            # Ensure values stay positive and reasonable
            min_val = max(10, mean_target - 25)
            max_val = min(95, mean_target + 25)
            # Also ensure remaining value will be positive
            min_remaining = 5  # Minimum final value
            max_allowed = remaining - min_remaining - (size - 1 - i - 1) * min_val
            max_val = min(max_val, max_allowed)
            val = random.randint(min_val, max(min_val, max_val))
            values.append(val)
            remaining -= val

        values.append(remaining)
        random.shuffle(values)

        values_str = ", ".join(str(v) for v in values)
        problem = f"Find the mean of the following data set: {values_str}"

        steps_list = []
        steps_list.append(step("STAT_SETUP", values_str))

        sum_expr = " + ".join(str(v) for v in values)
        total = sum(values)
        steps_list.append(step("STAT_SUM", sum_expr, total))
        steps_list.append(step("STAT_COUNT", size))
        steps_list.append(step("STAT_DIVIDE", f"{total} / {size}", mean_target))

        final_answer = str(mean_target)
        steps_list.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="mean",
            problem=problem,
            steps=steps_list,
            final_answer=final_answer,
        )


class MedianGenerator(ProblemGenerator):
    """
    Generates median calculation problems.

    Median is the middle value when data is ordered.
    - Odd count: middle value
    - Even count: average of two middle values

    Op-codes used:
    - STAT_SETUP: Set up the dataset (values)
    - STAT_ORDER: Order the values (ordered_values)
    - STAT_MIDDLE: Identify middle position(s) (position(s), value(s))
    - STAT_AVERAGE: Average middle values if needed (calculation, result)
    - Z: Final answer
    """

    def __init__(self, force_odd: bool = None):
        """
        Initialize generator.

        Args:
            force_odd: If True, use odd count; if False, use even count; if None, random
        """
        self.force_odd = force_odd

    def generate(self) -> dict:
        """Generate a median calculation problem."""
        if self.force_odd is True:
            size = random.choice([5, 7, 9])
        elif self.force_odd is False:
            size = random.choice([6, 8, 10])
        else:
            size = random.randint(5, 10)

        values = [random.randint(10, 99) for _ in range(size)]
        values_str = ", ".join(str(v) for v in values)

        problem = f"Find the median of the following data set: {values_str}"

        steps_list = []
        steps_list.append(step("STAT_SETUP", values_str))

        ordered = sorted(values)
        ordered_str = ", ".join(str(v) for v in ordered)
        steps_list.append(step("STAT_ORDER", ordered_str))

        if size % 2 == 1:
            # Odd: single middle value
            mid_idx = size // 2
            median = ordered[mid_idx]
            steps_list.append(step("STAT_MIDDLE", f"position {mid_idx + 1}", median))
            final_answer = str(median)
        else:
            # Even: average of two middle values
            mid_idx1 = size // 2 - 1
            mid_idx2 = size // 2
            val1 = ordered[mid_idx1]
            val2 = ordered[mid_idx2]
            median = (val1 + val2) / 2
            steps_list.append(step("STAT_MIDDLE", f"positions {mid_idx1 + 1} and {mid_idx2 + 1}", f"{val1}, {val2}"))
            steps_list.append(step("STAT_AVERAGE", f"({val1} + {val2}) / 2", median))

            if median == int(median):
                final_answer = str(int(median))
            else:
                final_answer = str(median)

        steps_list.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="median",
            problem=problem,
            steps=steps_list,
            final_answer=final_answer,
        )


class ModeGenerator(ProblemGenerator):
    """
    Generates mode calculation problems.

    Mode is the value(s) that appear most frequently.

    Op-codes used:
    - STAT_SETUP: Set up the dataset (values)
    - STAT_FREQUENCY: Show frequency count (value, count)
    - STAT_MODE: Identify mode(s) (mode_value(s), frequency)
    - Z: Final answer
    """

    def __init__(self, mode_type: str = None):
        """
        Initialize generator.

        Args:
            mode_type: One of 'unimodal', 'bimodal', 'no_mode' or None for random
        """
        valid_types = ['unimodal', 'bimodal', 'no_mode']
        if mode_type is not None and mode_type not in valid_types:
            raise ValueError(f"Invalid mode_type: {mode_type}. Must be one of {valid_types} or None.")
        self.mode_type = mode_type

    def generate(self) -> dict:
        """Generate a mode calculation problem."""
        mode_type = self.mode_type or random.choice(['unimodal', 'bimodal', 'no_mode'])

        if mode_type == 'unimodal':
            return self._generate_unimodal()
        elif mode_type == 'bimodal':
            return self._generate_bimodal()
        else:
            return self._generate_no_mode()

    def _generate_unimodal(self) -> dict:
        """Generate dataset with one mode."""
        mode_value = random.randint(20, 80)
        mode_freq = random.randint(3, 4)

        values = [mode_value] * mode_freq

        # Add other values with lower frequency
        other_values = random.sample([x for x in range(10, 100) if x != mode_value], 5)
        for v in other_values:
            freq = random.randint(1, mode_freq - 1)
            values.extend([v] * freq)

        random.shuffle(values)
        values_str = ", ".join(str(v) for v in values)

        problem = f"Find the mode of the following data set: {values_str}"

        steps_list = []
        steps_list.append(step("STAT_SETUP", values_str))

        # Count frequencies
        freq_dict = {}
        for v in values:
            freq_dict[v] = freq_dict.get(v, 0) + 1

        for val, count in sorted(freq_dict.items()):
            steps_list.append(step("STAT_FREQUENCY", val, count))

        steps_list.append(step("STAT_MODE", mode_value, mode_freq))

        final_answer = str(mode_value)
        steps_list.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="mode",
            problem=problem,
            steps=steps_list,
            final_answer=final_answer,
        )

    def _generate_bimodal(self) -> dict:
        """Generate dataset with two modes."""
        mode1 = random.randint(20, 50)
        mode2 = random.randint(60, 90)
        mode_freq = random.randint(3, 4)

        values = [mode1] * mode_freq + [mode2] * mode_freq

        # Add other values with lower frequency
        other_values = random.sample([x for x in range(10, 100) if x not in [mode1, mode2]], 4)
        for v in other_values:
            freq = random.randint(1, mode_freq - 1)
            values.extend([v] * freq)

        random.shuffle(values)
        values_str = ", ".join(str(v) for v in values)

        problem = f"Find the mode of the following data set: {values_str}"

        steps_list = []
        steps_list.append(step("STAT_SETUP", values_str))

        freq_dict = {}
        for v in values:
            freq_dict[v] = freq_dict.get(v, 0) + 1

        for val, count in sorted(freq_dict.items()):
            steps_list.append(step("STAT_FREQUENCY", val, count))

        steps_list.append(step("STAT_MODE", f"{mode1} and {mode2}", mode_freq))

        final_answer = f"{mode1} and {mode2}"
        steps_list.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="mode_bimodal",
            problem=problem,
            steps=steps_list,
            final_answer=final_answer,
        )

    def _generate_no_mode(self) -> dict:
        """Generate dataset with no mode (all values appear once)."""
        size = random.randint(6, 10)
        values = random.sample(range(10, 100), size)

        values_str = ", ".join(str(v) for v in values)

        problem = f"Find the mode of the following data set: {values_str}"

        steps_list = []
        steps_list.append(step("STAT_SETUP", values_str))

        for v in sorted(values):
            steps_list.append(step("STAT_FREQUENCY", v, 1))

        steps_list.append(step("STAT_MODE", "No mode", "All values appear with same frequency"))

        final_answer = "No mode"
        steps_list.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="mode_none",
            problem=problem,
            steps=steps_list,
            final_answer=final_answer,
        )


class RangeGenerator(ProblemGenerator):
    """
    Generates range calculation problems.

    Range = Maximum value - Minimum value

    Op-codes used:
    - STAT_SETUP: Set up the dataset (values)
    - STAT_MIN: Identify minimum (min_value)
    - STAT_MAX: Identify maximum (max_value)
    - STAT_RANGE: Calculate range (calculation, result)
    - Z: Final answer
    """

    def generate(self) -> dict:
        """Generate a range calculation problem."""
        size = random.randint(6, 12)
        values = [random.randint(10, 99) for _ in range(size)]

        values_str = ", ".join(str(v) for v in values)

        problem = f"Find the range of the following data set: {values_str}"

        steps_list = []
        steps_list.append(step("STAT_SETUP", values_str))

        min_val = min(values)
        max_val = max(values)
        range_val = max_val - min_val

        steps_list.append(step("STAT_MIN", min_val))
        steps_list.append(step("STAT_MAX", max_val))
        steps_list.append(step("STAT_RANGE", f"{max_val} - {min_val}", range_val))

        final_answer = str(range_val)
        steps_list.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="range",
            problem=problem,
            steps=steps_list,
            final_answer=final_answer,
        )


class MeanAbsoluteDeviationGenerator(ProblemGenerator):
    """
    Generates Mean Absolute Deviation (MAD) problems.

    MAD = (Σ|value - mean|) / n

    Op-codes used:
    - STAT_SETUP: Set up the dataset (values)
    - STAT_MEAN: Calculate mean (calculation, result)
    - STAT_DEVIATION: Calculate each deviation (value, mean, deviation)
    - STAT_ABS_DEV: Take absolute value (deviation, abs_deviation)
    - STAT_MAD: Calculate MAD (sum_of_abs_dev, count, result)
    - Z: Final answer
    """

    def generate(self) -> dict:
        """Generate a MAD calculation problem."""
        size = random.randint(5, 7)  # Keep small for reasonable calculations

        # Generate values that give a clean mean
        mean_target = random.randint(20, 50)
        total = mean_target * size

        values = []
        remaining = total
        for i in range(size - 1):
            val = random.randint(mean_target - 15, mean_target + 15)
            values.append(val)
            remaining -= val

        values.append(remaining)
        random.shuffle(values)

        values_str = ", ".join(str(v) for v in values)

        problem = f"Find the Mean Absolute Deviation (MAD) of the following data set: {values_str}"

        steps_list = []
        steps_list.append(step("STAT_SETUP", values_str))

        # Calculate mean
        mean = sum(values) / size
        mean_rounded = int(mean) if mean == int(mean) else round(mean, 2)
        steps_list.append(step("STAT_MEAN", f"{sum(values)} / {size}", mean_rounded))

        # Calculate deviations
        abs_devs = []
        # Round mean for display
        mean_display = int(mean) if mean == int(mean) else round(mean, 2)
        for v in values:
            dev = v - mean
            abs_dev = abs(dev)
            abs_devs.append(abs_dev)
            # Round deviations for display
            dev_display = int(dev) if dev == int(dev) else round(dev, 2)
            abs_dev_display = int(abs_dev) if abs_dev == int(abs_dev) else round(abs_dev, 2)
            steps_list.append(step("STAT_DEVIATION", v, mean_display, dev_display))
            steps_list.append(step("STAT_ABS_DEV", dev_display, abs_dev_display))

        # Calculate MAD
        sum_abs_devs = sum(abs_devs)
        mad = sum_abs_devs / size

        # Round for clean display
        if mad == int(mad):
            mad_display = int(mad)
            final_answer = str(mad_display)
        else:
            mad_display = round(mad, 2)
            final_answer = str(mad_display)

        # Also round sum_abs_devs for display if needed
        if sum_abs_devs == int(sum_abs_devs):
            sum_abs_devs_display = int(sum_abs_devs)
        else:
            sum_abs_devs_display = round(sum_abs_devs, 2)

        steps_list.append(step("STAT_MAD", sum_abs_devs_display, size, mad_display))

        steps_list.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="mean_absolute_deviation",
            problem=problem,
            steps=steps_list,
            final_answer=final_answer,
        )
