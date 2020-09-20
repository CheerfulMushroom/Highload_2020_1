import re

if __name__ == "__main__":
    file = open('helpers/results.txt')
    lines = file.readlines()

    req_line_pattern = r"GET /lol_(\d+)\.txt HTTP/1\.1"
    req_lin_regex = re.compile(req_line_pattern)

    all_indices = []

    for line in lines:
        match = req_lin_regex.match(line)
        if match:
            all_indices.append(int(match.group(1)))

    all_indices.sort()

    expected = [i for i in range(all_indices[0], all_indices[-1] + 1)]

    print('FOUND: {}/{}'.format(len(all_indices), len(expected)))

    if expected == all_indices:
        print('SUCCESS')
    else:
        print('FAIL')

        list_difference = []
        for item in expected:
            if item not in all_indices:
                list_difference.append(item)
        print('Did not find following indices')
        print(list_difference)
