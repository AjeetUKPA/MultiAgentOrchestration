def handle_interrupt(interrupt):
    action_request = interrupt.value["action_requests"][0]

    tool_name = action_request["name"]
    args = action_request["args"]

    print("\nTool execution requested")
    print(f"Tool: {tool_name}")
    print("Arguments:")
    for k, v in args.items():
        print(f"  {k}: {v}")

    decision = input("\nApprove? (y = approve, e = edit, n = reject): ").lower()

    if decision == "y":
        return {"type": "approve"}

    elif decision == "n":
        return {"type": "reject"}

    elif decision == "e":
        # allow modification
        print("\nEdit values (leave blank to keep current):")
        for k in args:
            new_val = input(f"{k} [{args[k]}]: ")
            if new_val.strip():
                args[k] = new_val

        return {
            "type": "edit",
            "args": args
        }

    else:
        return {"type": "reject"}