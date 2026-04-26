"""Smart study planner using fuzzy logic."""

from __future__ import annotations

from typing import Dict, Tuple


def triangular(value: float, left: float, peak: float, right: float) -> float:
    if value <= left or value >= right:
        return 0.0
    if value == peak:
        return 1.0
    if value < peak:
        return (value - left) / (peak - left)
    return (right - value) / (right - peak)


def trapezoid(value: float, left: float, left_top: float, right_top: float, right: float) -> float:
    if value <= left or value >= right:
        return 0.0
    if left == left_top and value == left:
        return 1.0
    if right == right_top and value == right:
        return 1.0
    if value < left_top:
        return (value - left) / (left_top - left)
    if value <= right_top:
        return 1.0
    return (right - value) / (right - right_top)


def fuzzify_energy_level(energy: float) -> Dict[str, float]:
    return {
        "low": trapezoid(energy, 0.0, 0.0, 3.5, 5.5),
        "medium": trapezoid(energy, 3.0, 4.5, 5.5, 7.5),
        "high": trapezoid(energy, 6.0, 7.5, 10.0, 10.0),
    }


def fuzzify_time_available(hours: float) -> Dict[str, float]:
    return {
        "short": trapezoid(hours, 0.0, 0.0, 1.5, 3.0),
        "medium": trapezoid(hours, 1.5, 2.5, 4.5, 6.0),
        "long": trapezoid(hours, 4.0, 5.5, 8.0, 8.0),
    }


def fuzzify_complexity(complexity: float) -> Dict[str, float]:
    return {
        "easy": trapezoid(complexity, 0.0, 0.0, 2.5, 4.5),
        "moderate": trapezoid(complexity, 3.5, 4.5, 6.5, 8.0),
        "hard": trapezoid(complexity, 6.0, 7.5, 10.0, 10.0),
    }


def apply_rules(energy: Dict[str, float], time_avail: Dict[str, float], complexity: Dict[str, float]) -> Dict[str, float]:
    outputs: Dict[str, float] = {
        "session_length": 0.0,
        "focus_level": 0.0,
        "rest_needed": 0.0,
    }
    weights: Dict[str, float] = {
        "session_length": 0.0,
        "focus_level": 0.0,
        "rest_needed": 0.0,
    }

    def add(rule_strength: float, session: float, focus: float, rest: float) -> None:
        outputs["session_length"] += rule_strength * session
        outputs["focus_level"] += rule_strength * focus
        outputs["rest_needed"] += rule_strength * rest
        weights["session_length"] += rule_strength
        weights["focus_level"] += rule_strength
        weights["rest_needed"] += rule_strength

    # Rule set
    add(min(energy["high"], time_avail["long"], complexity["easy"]), 3.0, 90.0, 10.0)
    add(min(energy["high"], time_avail["long"], complexity["moderate"]), 2.5, 85.0, 15.0)
    add(min(energy["high"], time_avail["medium"], complexity["moderate"]), 2.25, 85.0, 15.0)
    add(min(energy["medium"], time_avail["medium"], complexity["moderate"]), 1.75, 75.0, 20.0)
    add(min(energy["medium"], time_avail["short"], complexity["easy"]), 1.0, 70.0, 25.0)
    add(min(energy["low"], time_avail["short"], complexity["hard"]), 0.5, 50.0, 40.0)
    add(min(energy["low"], time_avail["medium"], complexity["easy"]), 1.0, 55.0, 35.0)
    add(min(energy["high"], time_avail["short"], complexity["hard"]), 1.25, 80.0, 20.0)
    add(min(energy["medium"], time_avail["long"], complexity["hard"]), 1.75, 70.0, 30.0)
    add(min(energy["low"], time_avail["long"], complexity["moderate"]), 1.25, 60.0, 35.0)
    add(min(energy["medium"], time_avail["short"], complexity["hard"]), 0.75, 65.0, 30.0)

    return {
        "session_length": outputs["session_length"] / max(weights["session_length"], 1e-6),
        "focus_level": outputs["focus_level"] / max(weights["focus_level"], 1e-6),
        "rest_needed": outputs["rest_needed"] / max(weights["rest_needed"], 1e-6),
    }


def infer_study_plan(energy: float, hours_available: float, complexity: float) -> Dict[str, float]:
    energy = max(0.0, min(10.0, energy))
    hours_available = max(0.0, min(8.0, hours_available))
    complexity = max(0.0, min(10.0, complexity))

    energy_fuzz = fuzzify_energy_level(energy)
    time_fuzz = fuzzify_time_available(hours_available)
    complexity_fuzz = fuzzify_complexity(complexity)

    result = apply_rules(energy_fuzz, time_fuzz, complexity_fuzz)
    return {
        "energy": energy,
        "time_available": hours_available,
        "complexity": complexity,
        "session_length_hours": round(result["session_length"], 2),
        "focus_percentage": round(result["focus_level"], 1),
        "rest_minutes": round(result["rest_needed"], 1),
    }


def format_plan(plan: Dict[str, float]) -> str:
    return (
        f"Smart Study Plan:\n"
        f"  Energy level: {plan['energy']}/10\n"
        f"  Time available: {plan['time_available']} hours\n"
        f"  Task complexity: {plan['complexity']}/10\n"
        f"  Suggested session length: {plan['session_length_hours']} hours\n"
        f"  Recommended focus intensity: {plan['focus_percentage']}%\n"
        f"  Suggested rest after session: {plan['rest_minutes']} minutes\n"
    )


def prompt_float(prompt_text: str, minimum: float, maximum: float) -> float:
    while True:
        try:
            value = float(input(prompt_text).strip())
            if minimum <= value <= maximum:
                return value
            print(f"Please enter a number between {minimum} and {maximum}.")
        except ValueError:
            print("Please enter a valid number.")


def main() -> None:
    print("Smart Study Planner — fuzzy logic recommendation")
    energy = prompt_float("Enter your current energy level (0-10): ", 0.0, 10.0)
    hours_available = prompt_float("Enter how many hours you can study (0-8): ", 0.0, 8.0)
    complexity = prompt_float("Enter task complexity (0=easy, 10=hard): ", 0.0, 10.0)

    plan = infer_study_plan(energy, hours_available, complexity)
    print("\n" + format_plan(plan))


if __name__ == "__main__":
    main()
