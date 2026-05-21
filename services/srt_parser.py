def parse_srt_blocks(lines):
    blocks = []
    block = []

    for line in lines:
        line = line.rstrip("\n")
        if line.strip() == "":
            if block:
                blocks.append(block)
                block = []
        else:
            block.append(line)

    if block:
        blocks.append(block)

    return blocks
