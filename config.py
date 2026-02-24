ALLOWED_TOOLS = ["nmap", "ping", "nslookup", "dig"]

TOOL_DESCRIPTIONS = """
Available Tools:
nmap:
- Network Scanner
- Use for port scanning and service detection
- Example: nmap --top-ports 100 <target>

ping:
- Test network connectivity
- Example: ping -c 4 <target>

nslookup:
- DNS lookup
- Example: nslookup <target>

dig:
- Advanced DNS lookup
- Example: dig <target>
"""