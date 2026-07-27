import json

edits = [
    ("work/notebooks/w03_data_contract.ipynb", 4,
     'print(contract_df["bucket"].value_counts())\nprint()\nprint(contract_df.to_string(index=False))\n',
     'print(contract_df["bucket"].value_counts())\ncontract_df\n'),

    ("work/notebooks/w03_feature_leakage_check.ipynb", 4,
     'notes_df = pd.DataFrame(feature_notes, columns=["feature", "meaning", "missing_handling", "available_before_prediction"])\nprint(notes_df.to_string(index=False))\n',
     'notes_df = pd.DataFrame(feature_notes, columns=["feature", "meaning", "missing_handling", "available_before_prediction"])\nnotes_df\n'),

    ("work/notebooks/w04_baseline_score.ipynb", 2,
     'print("\\nSignal 2 — Position vs CTR")\nprint(signal2_table)\n',
     'print("\\nSignal 2 — Position vs CTR")\nsignal2_table\n'),

    ("work/notebooks/w04_baseline_score.ipynb", 6,
     'print(f"Wrote {len(queue)} rows to baseline_action_score.csv")\nprint(queue.head(10))',
     'print(f"Wrote {len(queue)} rows to baseline_action_score.csv")\nqueue.head(10)'),

    ("work/notebooks/w04_baseline_score.ipynb", 8,
     'top10 = df_pos.sort_values("score", ascending=False).head(10)\nprint(top10[["content_id", "avg_position", "impressions_90d", "ctr", "score", "reason_code", "action"]])',
     'top10 = df_pos.sort_values("score", ascending=False).head(10)\ntop10[["content_id", "avg_position", "impressions_90d", "ctr", "score", "reason_code", "action"]]'),

    ("work/notebooks/w05_model.ipynb", 6,
     'comparison.loc[len(comparison)] = ["base_rate (test set)", round(y_test.mean(), 3), None, None]\nprint(comparison.to_string(index=False))',
     'comparison.loc[len(comparison)] = ["base_rate (test set)", round(y_test.mean(), 3), None, None]\ncomparison'),

    ("work/notebooks/w05_model.ipynb", 8,
     'print("\\nA sample of the wrong ones:")\nwrong_cols = ["content_id", "avg_position", "impressions_90d", "ctr", "trend_direction", "predicted_prob"]\nprint(top50.loc[top50["actual_label"] == 0, wrong_cols].head(6).to_string(index=False))',
     'print("\\nA sample of the wrong ones:")\nwrong_cols = ["content_id", "avg_position", "impressions_90d", "ctr", "trend_direction", "predicted_prob"]\ntop50.loc[top50["actual_label"] == 0, wrong_cols].head(6)'),

    ("work/notebooks/w06_validation_audit.ipynb", 8,
     'print("\\nA few concrete false negatives -- actual decliners the model missed:")\nprint(false_neg.sort_values("predicted_prob")[cols].head(4).to_string(index=False))',
     'print("\\nA few concrete false negatives -- actual decliners the model missed:")\nfalse_neg.sort_values("predicted_prob")[cols].head(4)'),

    ("work/notebooks/w07_action_playbook.ipynb", 2,
     'print(queue["action"].value_counts())\nprint("\\nTop 10 of the ranked queue:")\nprint(queue[["content_id", "action", "reason_code", "avg_position", "impressions_90d", "decline_prob"]].head(10).to_string(index=False))',
     'print(queue["action"].value_counts())\nprint("\\nTop 10 of the ranked queue:")\nqueue[["content_id", "action", "reason_code", "avg_position", "impressions_90d", "decline_prob"]].head(10)'),
]

by_file = {}
for path, idx, old, new in edits:
    by_file.setdefault(path, []).append((idx, old, new))

for path, changes in by_file.items():
    with open(path) as f:
        nb = json.load(f)
    for idx, old, new in changes:
        src = "".join(nb["cells"][idx]["source"])
        if old not in src:
            print(f"SKIP (already patched or changed): {path} cell {idx}")
            continue
        src = src.replace(old, new)
        nb["cells"][idx]["source"] = src.splitlines(keepends=True)
        nb["cells"][idx]["outputs"] = []
        nb["cells"][idx]["execution_count"] = None
    with open(path, "w") as f:
        json.dump(nb, f, indent=1)
    print(f"patched {path}: {len(changes)} cell(s)")

print("\nDone patching. Now re-run each notebook (Runtime -> Run All in Colab or Jupyter,")
print("or use nbclient) before committing, so the outputs actually reflect the cleaner tables.")
