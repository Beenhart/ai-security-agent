import subprocess
import ollama

# Run shell commands
def run_command(command):

    print(f"[+] Executing: {command}")

    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    return result.stdout

# Save report to file
def save_report(target, history):

    filename = f"reports/{target.replace('.', '_')}_report.txt"

    with open(filename, "w") as f:
        f.write(history)

    print(f"\n[+] Report saved to {filename}")

# Ask LLM what to do next
def decide_next_action(goal, current_data):

    prompt = f"""
You are a cybersecurity agent.

Goal: {goal}

Current data:
{current_data}

Decide the next command to run.

Rules:
- Only suggest ONE command
- Use tools like: nmap, ping, nslookup
- Never scan full port range (1-65535)
- Prefer top ports: use nmap --top-ports 1000 or less
- Avoid repeating the same scan
- If enough information gathered, say: DONE

Respond with only the command or DONE.
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['message']['content'].strip()


def main():

    target = input("Enter target: ")

    goal = f"Assess security of {target}"

    history = ""

    for i in range(5):  # limit steps

        print(f"\n=== Agent Step {i+1} ===")

        action = decide_next_action(goal, history)

        if "DONE" in action.upper():
            print("[+] Agent finished.")
            break

        output = run_command(action)

        history += f"\nCommand: {action}\nOutput: {output}\n"

        print(output)
        save_report(target, history)


if __name__ == "__main__":
    main()