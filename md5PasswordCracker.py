import hashlib


def crack_hash(target_hash, wordlist_path='dictionary.txt'):
    with open(wordlist_path, 'r') as file:
        for line in file:
            word = line.strip()
            hashed_word = hashlib.md5(word.encode()).hexdigest()
            if hashed_word == target_hash:
                return word  # Return the cracked password if found
    return None  # Return None if password not found
