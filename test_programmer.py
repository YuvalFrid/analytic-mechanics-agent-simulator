import sys
import os
sys.path.append(os.path.dirname(__file__))

from src.agents.parser import run_parser
from src.agents.solver import run_solver
from src.agents.programmer import run_programmer
def test_parser(user_input: str):
    print(f"\nInput: {user_input}")
    print("=" * 60)
    
    problem = run_parser(user_input)
    
    if problem is None:
        print("Parser returned None - check errors above")
        return

    print(f"Description:    {problem.problem_description}")
    print(f"Potential:      {problem.potential}")
    print(f"Type:           {problem.question_type}")
    print(f"Parameters:     {problem.parameters}")
    print(f"x(0):           {problem.initial_location}")
    print(f"v(0):           {problem.initial_velocity}")
    print(f"p(0):           {problem.initial_momentum}")
    test_solver(problem)


def test_solver(user_input: str):
    print("SOLVER")
    print("=" * 60)
    equations = run_solver(user_input)

    print(f"Potential:      {equations.potential}")
    print(f"Mass:      {equations.mass}")
    print(f"Type:           {equations.question_type}")
    print(f"Parameters:     {equations.parameters}")
    print(f"x(0):           {equations.initial_location}")
    print(f"v(0):           {equations.initial_velocity}")
    print(f"p(0):           {equations.initial_momentum}")
    print(f"Lagrange Equations:      {equations.lagrange_equation}")
    print(f"Hamilton Equations:      {equations.hamilton_equation}")
    test_programmer(equations)

def test_programmer(user_input: str):
    print("PROGRAMMER")
    print("=" *60)
    code = run_programmer(user_input)
    with open("output/simulation.py", "w") as f:
        f.write(code)

if __name__ == "__main__":
#    test_parser("A harmonic oscillator with k=5 and m=2, starting at x=1 with velocity 0")
    test_parser("A particle in a double well potential V(x) = -ax²/2 + bx⁴/4 with mass m=1, x(0)=0, p(0)=1")
#    test_parser("What is the capital of France?")
