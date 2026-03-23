import pandas as pd
from datetime import datetime


def log_decision(strategy, selected_assets, growth_weight):

    log_entry = {
        "Timestamp": datetime.now(),
        "Strategy": strategy,
        "Growth_Weight": growth_weight,
        "Selected_Assets": ", ".join(selected_assets)
    }

    new_log = pd.DataFrame([log_entry])

    try:
        existing_log = pd.read_csv("decision_audit_log.csv")
        updated_log = pd.concat([existing_log, new_log], ignore_index=True)
    except:
        updated_log = new_log

    updated_log.to_csv("decision_audit_log.csv", index=False)