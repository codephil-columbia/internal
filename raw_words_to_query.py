
formatted_lines = []

def get_coco_formatted(raw_line):
	return "(uuid_generate_v4(), '%s', 'coco')" % raw_line.rstrip()

def get_spacerace_formatted(raw_line):
	return "(uuid_generate_v4(), '%s', 'spacerace')" % raw_line.rstrip()

def get_boatrace_formatted(raw_line):
	temp_string = "(uuid_generate_v4(), '%s', 'boatrace')" % raw_line.rstrip()
	return temp_string.replace("\n", "\\n")

temp_spacerace_line = ""

with open('boatrace_words.txt') as fp:
	line = fp.readline()

	temp_spacerace_line += line

	# formatted_line = get_spacerace_formatted(line)
	# formatted_lines.append(formatted_line)

	while line:
		line = fp.readline()

		if line == "//\n":
			formatted_line = get_boatrace_formatted(temp_spacerace_line)
			formatted_lines.append(formatted_line)
			temp_spacerace_line = ""
		else:
			temp_spacerace_line += line



# with open('spacerace_words.txt') as fp:
# 	line = fp.readline()

# 	formatted_line = get_spacerace_formatted(line)
# 	formatted_lines.append(formatted_line)

# 	while line:
# 		line = fp.readline()

# 		formatted_line = get_spacerace_formatted(line)
# 		formatted_lines.append(formatted_line)

for item in formatted_lines:
	print item