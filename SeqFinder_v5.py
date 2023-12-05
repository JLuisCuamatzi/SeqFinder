#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jcuamatzi
@ execute: python3 SeqFinder_v4.py -f <input.fasta> -t <target_sequence>

## Any bug or comment should be reported to: cuamatzi.flores.jorge.de@outlook.com
"""

import argparse

# Function to parse arguments
def parse_arguments():
    """
    Parses command-line arguments for the script.

    Returns:
        argparse.Namespace: An object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fasta-file", required=True, help="fasta file ")
    parser.add_argument("-t", "--target-sequence-file", required=True, help="file containing the target sequence")
    return parser.parse_args()

# Function to read the target sequence file
def read_target_sequence(file_path):
    """
    Reads the target sequence from a file.

    Parameters:
    - file_path (str): The path to the file containing the target sequence.

    Returns:
    tuple: A tuple containing the target name and sequence.
    """
    with open(file_path, 'r') as target_file:
        lines = target_file.readlines()

        # Find the line starting with '>'
        for i, line in enumerate(lines):
            if line.startswith('>'):
                target_name = line[1:].strip()  # Extract the name after '>'
                # Join lines after '>' until the end of the file
                target_sequence = ''.join(lines[i+1:])
                break
        else:
            # If no line starting with '>' is found, use the entire content
            target_name = "UnknownTarget"
            target_sequence = ''.join(lines)

    return target_name, target_sequence.strip()

# Function to read the FASTA file
def read_fasta(file_path):
    """
    Reads a FASTA file and extracts sequences with their headers.

    Parameters:
    - file_path (str): The path to the FASTA file.

    Returns:
    dict: A dictionary where keys are sequence headers and values are the corresponding sequences.
    """
    sequences = {}
    current_header = ''
    current_sequence = ''

    with open(file_path, 'r') as fasta_file:
        for line in fasta_file:
            line = line.strip()
            if line.startswith('>'):
                if current_header:
                    sequences[current_header] = current_sequence
                    current_sequence = ''

                current_header = line[1:]
            else:
                current_sequence += line

        if current_header:
            sequences[current_header] = current_sequence

    return sequences

# Function to search the target sequence in the fasta file
def find_sequence(fasta_sequences, target_sequence):
    """
    Finds occurrences of a target sequence in a dictionary of FASTA sequences.

    Args:
        fasta_sequences (dict): Dictionary of FASTA sequences with headers as keys.
        target_sequence (str): The sequence to be searched.

    Returns:
        list: List of tuples with information about matches (header, start_pos, end_pos).
    """
    matches = []

    for header, sequence in fasta_sequences.items():
        sequence = sequence.replace('\n', '')
        start_pos = sequence.find(target_sequence)

        while start_pos != -1:
            end_pos = start_pos + len(target_sequence)
            matches.append((header, start_pos + 1, end_pos))
            start_pos = sequence.find(target_sequence, start_pos + 1)

    return matches

# Execute the code
def main():
    args = parse_arguments()

    fasta_file_path = args.fasta_file
    target_sequence_file_path = args.target_sequence_file

    target_name, target_sequence = read_target_sequence(target_sequence_file_path)
    sequences = read_fasta(fasta_file_path)
    matches = find_sequence(sequences, target_sequence)

    if not matches:
        print(f'Target "{target_name}" sequence not found.')
    else:
        if len(matches) == 1:
            print(f'Target "{target_name}" sequence has only one match:')
        else:
            print(f'Multiple matches found for the target "{target_name}" sequence:')

        for match in matches:
            header, start_pos, end_pos = match
            print(f"Header of reference sequence: {header}\nStart Position: {start_pos}\nEnd Position: {end_pos}\n---")

if __name__ == "__main__":
    main()

