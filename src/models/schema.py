from dataclasses import dataclass
from typing import Optional, List, Union, Dict
@dataclass
class ProblemDescription:
    problem_description: str
    potential: str
    question_type: str ## hamiltonian or lagrangian
    parameters: Dict[str,Optional[float]]
    initial_location: Optional[float]
    initial_velocity: Optional[float]
    initial_momentum: Optional[float]

@dataclass
class EquationsOfMotion:
    potential: str
    mass: Union[str,float]
    initial_location: Optional[float]
    initial_velocity: Optional[float]
    initial_momentum: Optional[float]
    question_type: str
    parameters: Dict[str,Optional[float]]
    lagrange_equation: Optional[str]
    hamilton_equation: Optional[str]

@dataclass
class InspectorReport:
    pass_loop: bool
    errors: List[str]
    agent_responsible: Optional[str]
    suggested_fix: Optional[str]


