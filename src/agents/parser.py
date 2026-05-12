import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.models.schema import ProblemDescription
from src.utils.llm_client import call_llm

MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """
Your job is to parse 1D Hamiltonian and Lagrangian mechanics problems.

Detect whether the problem requires a Hamiltonian or Lagrangian formulation:
- If initial momentum is given, use Hamiltonian
- If initial velocity is given, use Lagrangian
- If neither is given, default to Lagrangian

Extract the potential V(x), written as a Python-evaluable string using x as the position 
variable and ** for exponentiation. For example: "0.5 * k * x**2" or "-m * g * cos(x)".

Extract all parameters (mass, spring constant, etc.) as a dictionary of name to value.
If a parameter is mentioned but no value is given, set its value to null.

Return only a JSON object in exactly this format:
{
  "problem_description": "a harmonic oscillator with spring constant k=5 and mass m=2, starting at x=1 with v=0",
  "potential": "0.5 * k * x**2",
  "question_type": "lagrangian",
  "parameters": {"k": 5.0, "m": 2.0},
  "initial_location": 1.0,
  "initial_velocity": 0.0,
  "initial_momentum": null
}

If a parameter has no given value, set it to null:
  "parameters": {"k": null, "m": 2.0}

If the input is not a valid 1D mechanics problem, return:
  {"error": "Input is not a valid 1D mechanics problem"}

Return only valid JSON, no extra text.
"""


def parse_problem(response: dict) -> ProblemDescription:
    return ProblemDescription(
        problem_description=response["problem_description"],
        potential=response["potential"],
        question_type=response["question_type"],
        parameters=response["parameters"],
        initial_location=response.get("initial_location"),
        initial_velocity=response.get("initial_velocity"),
        initial_momentum=response.get("initial_momentum")
    )


def run_parser(user_input: str) -> ProblemDescription:
    response = call_llm(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_input,
        model=MODEL
    )

    if response is None:
        print("Parser: API call failed")
        return None

    if "error" in response:
        print(f"Parser: {response['error']}")
        return None

    return parse_problem(response)
