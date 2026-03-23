import pulp
import pandas as pd


def optimize_portfolio(df, strategy, max_assets=3):

    # Create optimization problem
    problem = pulp.LpProblem("Portfolio_Selection", pulp.LpMaximize)

    # Decision variables (0 or 1)
    decision_vars = {
        prop: pulp.LpVariable(prop, 0, 1, pulp.LpBinary)
        for prop in df["Property_ID"]
    }

    # Strategy scores dictionary
    scores = dict(zip(df["Property_ID"], df[strategy]))

    # Objective function (maximize total score)
    problem += pulp.lpSum(
        decision_vars[prop] * scores[prop]
        for prop in decision_vars
    )

    # Constraint: limit number of selected assets
    problem += pulp.lpSum(
        decision_vars[prop]
        for prop in decision_vars
    ) <= max_assets

    # Solve optimization
    problem.solve()

    selected_assets = [
        prop for prop in decision_vars
        if decision_vars[prop].value() == 1
    ]

    return selected_assets