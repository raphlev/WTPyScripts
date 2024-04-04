import re
from difflib import SequenceMatcher

# Normalize a string for comparison
def normalize_string(s):
    # Replace hyphens, slashes, and spaces with a single hyphen and convert to lowercase
    s = re.sub(r"[- /]", "-", s.lower())
    # Split the string into words and filter out those shorter than 3 characters
    words = [word for word in s.split() if len(word) > 2]
    return set(words)

# Find the best matching reference value for a given lookup value
def find_best_match(lookup_value, reference_values):
    lookup_words = normalize_string(lookup_value)
    best_match_score = 0
    best_match_value = ""
    # Compare the lookup value to each reference value
    for ref_value in reference_values:
        ref_words = normalize_string(ref_value)
        # Calculate a score based on common words and overall similarity
        score = (2 * len(lookup_words.intersection(ref_words)) / 
                 (len(lookup_words) + len(ref_words)) +
                 SequenceMatcher(None, lookup_value, ref_value).ratio()) / 3
        # Update the best match if this score is the highest so far
        if score > best_match_score:
            best_match_score = score
            best_match_value = ref_value
    return best_match_value, best_match_score

# Load data from files. Replace 'Reference_File.txt' and 'Lookup_File.txt'
# with the paths to your actual files.
with open("Reference_File.txt", "r", encoding='utf-8') as file:
    reference_values = file.read().splitlines()

with open("Lookup_File.txt", "r", encoding='utf-8') as file:
    lookup_values = file.read().splitlines()

# Dictionary to store each lookup value's best match
matches = {}
for lookup_value in lookup_values:
    best_match, score = find_best_match(lookup_value, reference_values)
    matches[lookup_value] = (best_match, score)

# Write the matches and their scores to a file named 'matched_results.txt'
with open("matched_results.txt", "w") as file:
    for lookup, match in matches.items():
        file.write(f"{lookup} => {match[0]} (Score: {match[1]:.4f})\n")

print("Matches have been saved to matched_results.txt.")

# Write the matches to a CSV file named 'matched_results.csv'
with open("matched_results.csv", "w", encoding='utf-8') as file:
    # Write the header
    file.write("Lookup;Reference\n")
    # Write each match
    for lookup, match in matches.items():
        file.write(f"{lookup};{match[0]}\n")

print("Matches have been saved to matched_results.csv.")

# How to execute:
# Save this script to a file, for example, "match_finder.py".
# Ensure Python is installed on your system.
# Run the script from a terminal or command prompt with the command:
# python match_finder.py
# Make sure 'Reference_File.txt' and 'Lookup_File.txt' are in the same directory as the script
# or adjust the file paths in the script accordingly.
