import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.models.schema import EquationsOfMotion, ProblemDescription
from src.utils.llm_client import call_llm

MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """
You are a classical mechanics equation solver. You will receive a JSON describing a 1D mechanics problem and must output the equations of motion as Python-evaluable strings.

Input format:
{
  "problem_description": "a harmonic oscillator with spring constant k=5 and mass m=2, starting at x=1 with v=0",
  "potential": "0.5 * k * x**2",
  "question_type": "lagrangian",
  "parameters": {"k": 5.0, "m": 2.0},
  "initial_location": 1.0,
  "initial_velocity": 0.0,
  "initial_momentum": null
}

Your job:
1. Compute dV/dx symbolically from the potential string
2. Substitute all known parameter values (non-null) into the equations
3. If a parameter is null, keep it as a symbolic name (e.g. k, m)
4. Write the right-hand side of each ODE as a Python-evaluable string using x, v, p as variables

For Lagrangian problems, output one equation:
- dv_dt: "-({dV/dx}) / {m}" with values substituted

For Hamiltonian problems, output one equation:
- dp_dt: "-({dV/dx})" with values substituted

Output format for Lagrangian example with k=5, m=2:
{
  "potential": "0.5 * k * x**2",
  "question_type": "lagrangian",
  "parameters": {"k": 5.0, "m": 2.0},
  "initial_location": 1.0,
  "initial_velocity": 0.0,
  "initial_momentum": null,
  "mass": 2.0,
  "lagrange_equation": "-(5.0 * x) / 2.0",
  "hamilton_equation": null
}

Output format for Hamiltonian example with k=5, m=2:
{
  "potential": "0.5 * k * x**2",
  "question_type": "hamiltonian",
  "parameters": {"k": 5.0, "m": 2.0},
  "initial_location": null,
  "initial_velocity": null,
  "initial_momentum": 0.0,
  "mass": 2.0,
  "lagrange_equation": null,
  "hamilton_equation": "-(5.0 * x)"
}

Return only valid JSON, no extra text.
"""


def parse_equations(response: dict) -> EquationsOfMotion:
    return EquationsOfMotion(
        potential=response["potential"],
        mass=response["mass"],
        initial_location=response.get("initial_location"),
        initial_velocity=response.get("initial_velocity"),
        initial_momentum=response.get("initial_momentum"),
        question_type=response["question_type"],
        parameters=response["parameters"],
        lagrange_equation=response.get("lagrange_equation"),
        hamilton_equation=response.get("hamilton_equation")
    )


def run_solver(problem: ProblemDescription) -> EquationsOfMotion:
    user_prompt = f"""
Solve this mechanics problem and return the equations of motion:
{problem.__dict__}
"""

    response = call_llm(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
        model=MODEL
    )

    if response is None:
        print("Solver: API call failed")
        return None

    if "error" in response:
        print(f"Solver: {response['error']}")
        return None

    return parse_equations(response)
