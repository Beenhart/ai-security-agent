MEMORY_FILE = "memory.txt"

def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return f.read()
    except:
        return ""
    
def save_memory(entry):
    with open(MEMORY_FILE, "a") as f:
        f.write(entry + "\n")
