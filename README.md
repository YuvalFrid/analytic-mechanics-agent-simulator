## What it does
This project is an agentic AI framework that converts printed diagrams of basic electric circuits into an interactive simulation, showing all equations describing the circuit and how the different component values affect each other.

## How it works
The first step is using a multimodal LLM (GPT-4o) named "Viewer" to parse the diagram into a structured JSON representation of the circuit called a "netlist". A feedback loop containing three agents starts running after that - "Electrician", "Programmer", and "Inspector". The Electrician turns the netlist into a JSON of variables and equations describing the circuit's behavior. The Programmer uses the netlist and the equations to create an interactive simulator using matplotlib and other Python libraries. The result is a standalone Python script that opens an interactive matplotlib window with sliders for each component value and live plots of voltage and current. The Inspector then verifies that the physics and math are correct, actively runs the generated code, and checks that the simulation behaves as expected. If any agent produces incorrect results, the Inspector writes a structured report and generates a targeted prompt for each failing agent to use in the next iteration.

## Setup
[placeholder for now]

## Limitations
- Only supports circuits with up to 10 basic components: resistors, capacitors, inductors, power sources, and grounding
- Input must be a clearly printed circuit diagram, not a hand-drawn sketch
