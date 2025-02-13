import re

def extract_lua_block(content, block_name):
    """Extracts a Lua block by name, including nested braces."""
    start = content.find(f"{block_name} = ")
    if start == -1:
        return "{}"

    brace_count = 0
    end = start
    in_string = False
    block_start = start + len(f"{block_name} = ")

    while end < len(content):
        char = content[end]

        if char == '"' and content[end - 1] != '\\':  # Handle quotes properly
            in_string = not in_string

        if not in_string:
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    return content[block_start:end + 1]  # Extract the full block

        end += 1

    return "{}"  # Return empty if it somehow fails

def extract_lua_table(content, table_name):
    """Extracts the full content of a Lua table given its name."""
    start = content.find(f'["{table_name}"] = ' + "{")
    if start == -1:
        return "{}"

    brace_count = 0
    end = start
    in_string = False

    while end < len(content):
        char = content[end]

        if char == '"' and content[end - 1] != '\\':  # Handle quotes properly
            in_string = not in_string

        if not in_string:
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    break

        end += 1

    return content[start + len(f'["{table_name}"] = '):end + 1]

def parse_lua_table(lua_string):
    """Parses a Lua table into a Python dictionary."""
    table = {}
    stack = [table]
    key = None
    current = table
    lua_string = lua_string.strip().strip("{}")

    lines = lua_string.split("\n")

    for line in lines:
        line = line.strip()
        if not line or line.startswith("--"):  # Ignore empty lines and comments
            continue

        key_match = re.match(r'\[(\d+|".+?")\]\s*=', line)
        if key_match:
            key = key_match.group(1).strip('"') if '"' in key_match.group(1) else int(key_match.group(1))
            value = line.split("=", 1)[1].strip()

            if value.startswith("{"):
                new_dict = {}
                current[key] = new_dict
                stack.append(current)
                current = new_dict
            else:
                value = value.strip(",")
                if value.isdigit():
                    value = int(value)
                elif value.startswith('"') and value.endswith('"'):
                    value = value.strip('"')
                current[key] = value

        elif line.startswith("}"):
            current = stack.pop()

    return table

def serialize_lua_table(data, indent=1):
    """Serializes a Python dictionary into a Lua table format."""
    result = "{\n"
    indent_str = "\t" * indent

    for key, value in data.items():
        key_str = f'["{key}"]' if isinstance(key, str) else f"[{key}]"

        if isinstance(value, dict):
            value_str = serialize_lua_table(value, indent + 1)
        elif isinstance(value, str):
            value_str = f'"{value}"'
        else:
            value_str = str(value)

        result += f"{indent_str}{key_str} = {value_str},\n"

    return result + ("\t" * (indent - 1)) + "}"

def deep_merge(target, source):
    """Recursively merges source dictionary into target."""
    for key, value in source.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            deep_merge(target[key], value)
        else:
            target[key] = value  # Overwrite with new data

# Read the Lua files
with open("Defaults.lua", "r", encoding="utf-8") as file:
    defaults_content = file.read()

with open("InFlight.lua", "r", encoding="utf-8") as file:
    inflight_content = file.read()

# Extract the profile section and preserve it
profile_section = extract_lua_block(defaults_content, "profile")

# Extract the Horde and Alliance tables from both files
defaults_horde = parse_lua_table(extract_lua_table(defaults_content, "Horde"))
defaults_alliance = parse_lua_table(extract_lua_table(defaults_content, "Alliance"))

inflight_horde = parse_lua_table(extract_lua_table(inflight_content, "Horde"))
inflight_alliance = parse_lua_table(extract_lua_table(inflight_content, "Alliance"))

# Merge the extracted data
deep_merge(defaults_horde, inflight_horde)
deep_merge(defaults_alliance, inflight_alliance)

# Reconstruct the full Defaults.lua structure with preserved profile
merged_output = f"""InFlight.defaults = {{
    profile = {profile_section},
    global = {{
        ["Horde"] = {serialize_lua_table(defaults_horde, 2)},
        ["Alliance"] = {serialize_lua_table(defaults_alliance, 2)}
    }}
}}
"""

# Write the merged output to Merged.lua
with open("Merged.lua", "w", encoding="utf-8") as file:
    file.write(merged_output)

print("Merged.lua has been successfully created!")
