def evaluate(manual_output, llm_output):

    def score(output):
        if not output:
            return 0
        if isinstance(output, dict) and len(output) > 0:
            return 2
        return 1

    manual_score = score(manual_output)
    llm_score = score(llm_output)

    if llm_score > manual_score:
        return {
            "chosen_method": "llm",
            "confidence": "high" if llm_score == 2 else "medium",
            "output": llm_output
        }
    else:
        return {
            "chosen_method": "manual",
            "confidence": "high" if manual_score == 2 else "medium",
            "output": manual_output
        }