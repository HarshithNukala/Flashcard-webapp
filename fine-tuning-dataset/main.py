import json

in_path = "flashcard_dataset.jsonl"        # original file
out_path = "flashcard_dataset.jsonl" # new file with answer as string

with open(in_path, "r", encoding="utf-8") as fin, open(out_path, "w", encoding="utf-8") as fout:
    for line_no, line in enumerate(fin, start=1):
        line = line.strip()
        if not line:
            continue  # skip empty lines

        try:
            ex = json.loads(line)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON parse error on line {line_no}: {e}") from e

        # Only change MCQ examples
        if ex.get("task_type") == "mcq":
            target = ex.get("target", {})
            if "answer" in target:
                # Convert int -> string (or any type -> string)
                target["answer"] = str(target["answer"])
                ex["target"] = target

        # Write back as JSONL
        fout.write(json.dumps(ex, ensure_ascii=False) + "\n")

print("Done! Saved fixed file to:", out_path)
