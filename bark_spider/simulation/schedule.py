from brooks.state import State
from brooks.communication import (
    gompertz_overhead_proportion,
)


class Schedule:
    def __init__(self, state, interventions):
        self._state = state
        self._interventions = sorted(interventions, key=lambda i: i.time)

    def initial(self):
        """Configure the initial model state."""
        return self._state

    def intervene(self, step_number, elapsed_time, state):
        """Intervene in the current step before the main simulation step is
        executed.
        """
        while (self._interventions and
               self._interventions[0].time <= elapsed_time):
            state = self._interventions[0].apply(state)
            self._interventions = self._interventions[1:]

        return state

    def is_complete(self, step_number, elapsed_time_seconds, state):
        """Determine whether the simulation should end."""
        return state.num_function_points_developed >= \
            state.num_function_points_requirements

    def complete(self, step_number, elapsed_time_seconds, state):
        """Finalise the simulation state for the last recorded step."""
        state.software_development_rate = 0
        return state


def make_schedule(assimilation_delay,
                  training_overhead_proportion,
                  interventions,
                  num_function_points_requirements=500,
                  **kwargs):
    """Create a new State object.

    Args:
        assimilation_delay: Numer of days needed to assimilate new developers.
        interventions: An iterable of `Intervention` instances.

    Returns:
        A new State object.
    """
    state = State(
        step_duration_days=1,
        num_function_points_requirements=num_function_points_requirements,
        num_function_points_developed=0,
        num_new_personnel=20,
        num_experienced_personnel=0,
        personnel_allocation_rate=0,
        personnel_assimilation_rate=0,
        assimilation_delay_days=assimilation_delay,
        nominal_productivity=0.1,
        new_productivity_weight=0.8,
        experienced_productivity_weight=1.2,
        training_overhead_proportion=training_overhead_proportion,
        communication_overhead_function=gompertz_overhead_proportion,
        software_development_rate=None,
        cumulative_person_days=0,
    )

    return Schedule(state, interventions)
