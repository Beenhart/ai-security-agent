import subprocess
import time
from click import command
import ollama

# Run shell commands
def run_command(command):

    print(f"[+] Executing: {command}")
    start_time = time.time()
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )
    end_time = time.time()
    duration = end_time - start_time
    print(f"[+] Command executed in {duration:.2f} seconds")
    return result.stdout, duration

# Save report to file
def save_report(target, history):

    filename = f"reports/{target.replace('.', '_')}_report.txt"

    with open(filename, "w") as f:
        f.write(history)

    print(f"\n[+] Report saved to {filename}")

# Ask LLM what to do next
def decide_next_action(goal, current_data, memory):

    prompt = f"""
You are a cybersecurity agent.

Goal: {goal}

Current data:
{current_data}

Long-term memory:
{memory}

Decide the next command to run.

Rules:
- Only suggest ONE command
- Use tools like: nmap, ping, nslookup
- Never scan full port range (1-65535)
- Prefer top ports: use nmap --top-ports 1000 or less
- Avoid repeating the same scan
- If enough information gathered, say: DONE

Respond EXACTLY in this format: 

REASON: your reasoning here
COMMAND: the command to execute

If finished, respond:

REASON: explanation
COMMAND: DONE
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    full_response = response['message']['content'].strip()

    print("\nAgent decision:")
    print(full_response)

    #Extract command
    if "COMMAND:" in full_response:
        command = full_response.split("COMMAND:")[1].strip()
    else:
        command = "DONE"
    
    return command

def load_memory():
    # Placeholder for loading past interactions or data
    try:
        with open("memory.txt", "r") as f:
            return f.read()
    except:
        return ""

def save_memory(new_data):
    # Placeholder for saving interactions or data
    with open("memory.txt", "a") as f:
        f.write(new_data + "\n")

def main():

    target = input("Enter target: ")

    goal = f"Assess security of {target}"

    current_data = ""
    history = ""
    memory = load_memory()
    i = 0
    for i in range(10):  # Limit to 10 iterations to avoid infinite loops

        print(f"\n=== Agent Step {i+1} ===")

        action = decide_next_action(goal, history, memory)

        if "DONE" in action.upper():
            print("[+] Agent finished.")
            break

        output = run_command(action)

        history += f"\nCommand: {action}\nOutput: {output}\n"
        save_memory(f"{target}: {action}")
        print(output)
        save_report(target, history)



if __name__ == "__main__":
    main()