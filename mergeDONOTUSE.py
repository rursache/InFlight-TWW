#This script does not seem to work and I am renaming it to indicate that it should not be used. Keeping it around for preservation purposes.
import re

def parse_lua_table(content, key):
    pattern = rf'{key}\s*=\s*{{(.*?)}}'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def merge_lua_files(inflight_path, defaults_path, output_path):
    # Read the contents of both files
    with open(inflight_path, 'r') as file:
        inflight_content = file.read()
    
    with open(defaults_path, 'r') as file:
        defaults_content = file.read()
    
    # Parse the relevant sections from InFlight.lua
    inflight_horde = parse_lua_table(inflight_content, r'\["Horde"\]')
    inflight_alliance = parse_lua_table(inflight_content, r'\["Alliance"\]')
    
    # Replace or add the Horde and Alliance data in the defaults content
    defaults_content = re.sub(
        r'(\["Horde"\]\s*=\s*{).*?(})',
        rf'\1{inflight_horde or ""}\2',
        defaults_content,
        flags=re.DOTALL
    )
    defaults_content = re.sub(
        r'(\["Alliance"\]\s*=\s*{).*?(})',
        rf'\1{inflight_alliance or ""}\2',
        defaults_content,
        flags=re.DOTALL
    )
    
    # Write the merged content to the output file
    with open(output_path, 'w') as file:
        file.write(defaults_content)

# Usage
merge_lua_files('InFlight.lua', 'Defaults.lua', 'Defaults-new.lua')


"""
Claude.ai prompt to generate this:
"""

"""
I want to merge the data from "InFlight.lua" with "Defaults.lua".

The "Defaults.lua" has the following structure:

```lua
InFlight.defaults = {
	profile = {},
	global = {
		["Horde"] = {},
		["Alliance"] = {}
	}
}
```

The contents of the "profile" key doesn't matter. All that matters is the contents of global["Horde"] and global["Alliance"]. Here is an example of the contents of global["Horde"] and global["Alliance"]:

```lua
["Horde"] = {
	[67] = {
		[12] = 544,
		[16] = 192,
		[19] = 835,
		[43] = 167,
		[45] = 669,
		[66] = 148
	}
}
```

Now I will show you the contents of the "InFlight.lua" file:

```lua
InFlightDB = {
	["version"] = "retail",
	["global"] = {
	},
	["Horde"] = {
	},
	["upload"] = 1720866296,
	["profileKeys"] = {
	},
	["dbinit"] = 920,
	["profiles"] = {
	}
}
```

As you can see, the structure is similar but in the "InFlight.lua" file there are more keys we should ignore.

I want you to write a script that will parse both files and then take the contents of global["Horde"] and global["Alliance"] from the "InFlight.lua" file and add them to the "Defaults.lua" file.

The formatting and file structure must be perserved. Also if the keys already exists in "Defaults.lua", they should have their values replaced with the ones from "InFlight.lua"

The final merged output should be written out as a "Merged.lua" file
"""
