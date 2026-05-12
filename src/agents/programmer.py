import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.models.schema import EquationsOfMotion, ProblemDescription
from src.utils.llm_client import call_llm, call_llm_raw

MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """
You are a classical mechanics equation programmer. You will receive a JSON describing the 1D mechanics equations from a mechanics problem and their parameters and initial conditions, and you will write a python code using numpy and scipy to solve it. After solving, you will use these solutions to plot a GUI with matplotlib, where the equations of motions are shown, and initial conditions or parameter values can be controlled manually by the user. 

Input format for Lagrangian example with k=5, m=2:
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

Input format for Hamiltonian example with k=5, m=2:
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

You will receive from the input one differential equation, and the second differential equation will always remain the same:
    for lagrangian problems it will be dx_dt = v, and for hamilton problems dx_dt = p/m. the equation inputs you receive are always dv_dt = "lagrange_equation" for lagrangians, and dp_dt = "hamilton_equation" for hamiltonians. 
    the initial conditions you will have to integrate yourself.
any parameter that isn't given as input will be set to 1 as a default.
In the GUI, you will display the 2 differential equation system, and the solution for each of the x and v/p. always use numerical integration with scipy.integrate.solve_ivp and display only the numerical solution. for any parameter (m,k,etc...) have a slider from 0.1x to 10x the value that the user can change to see the difference in the plots. 
Once you have the solutions for x(t) and (p/v)(t), you will draw three plots: 
    1. x(t) from t = 0 until t_max
    2. (p/v)(t) from t = 0 until t_max
    3. (p/v)(x) from x_min to x_max
pay attention - t_max is determined by both x and (p/v), such that the full range of motion can be shown at least once. x_min and x_max should be determined in the same way. If the motion isn't repetitive (not a potential well or harmonic oscillator etc...) just set hard limits to x_min = -100 and x_max = 100. 

Your job:
1. Write the 2 differential equation system in scipy and numpy 
2. Substitute all known parameter values (nulls are switched with 1) into the equations
3. Create a GUI showing the equations of motions explicitly, their solution, and three plots side by side for the motion x(t),(p/v)(t) and (p/v)(x) with the proper limits.
4. Add for all initial conditions and parameters a slider with range 0.1x to 10x.

Use matplotlib.widgets.Slider for all parameters and initial conditions.
Structure the figure as:
- Top section: three side by side plots
- Bottom section: sliders, one per parameter and initial condition
- Use fig.canvas.draw_idle() in the update function to refresh plots


Your output is an executable .py file. return nothing but that. 
IMPORTANT: Your response must contain ONLY the Python code. 
No explanations, no preamble, no markdown, no backticks. 
Start your response with "import" and end with the last line of code.

"""


def clean_code(raw: str) -> str:
    raw = raw.strip()
    if "```" in raw:
        # find the first ``` and take everything after it
        raw = raw.split("```", 1)[1]
        # remove the language identifier line (e.g. "python")
        raw = raw.split("\n", 1)[1]
        # remove closing ```
        if "```" in raw:
            raw = raw.rsplit("```", 1)[0]
    return raw.strip()


def run_programmer(equations: EquationsOfMotion) -> str:
    user_prompt = f"""
Solve these mechanics problem equations and return the executable .py with GUI:
{equations.__dict__}
"""

    response = call_llm_raw(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
        model=MODEL
    )

    if response is None:
        print("Programmer: API call failed")
        return None

    return clean_code(response)
