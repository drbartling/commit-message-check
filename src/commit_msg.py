#!/usr/bin/python

import os
import re
import sys

def LabelIsValid(label):
    valid_labels = set([
        'chore',
        'docs',
        'feat',
        'fix',
        'refactor',
        'revert',
        'style',
        'test',
    ])
    return label in valid_labels


def LabelFromSubject(subject):
    label = subject.split(":")[0]
    return label


def SubjectIsValid(subject):
    if SubjectHasLabel(subject) is not True:
        return False

    if SubjectLengthIsValid(subject) is not True:
        return False

    if SubjectIsCapitalized(subject) is not True:
        return False

    return True


def SubjectHasLabel(subject):
    label_format = re.compile(r"[a-zA-Z][a-z]*:")
    if not label_format.match(subject):
        print('Subject should be in the form of "<label>: <Subject>".')
        return False
    return True


def SubjectLengthIsValid(subject):
    soft_limit = 50
    hard_limit = soft_limit + 10
    if len(subject) > hard_limit:
        print("Subject line must be less than {} characters.".format(soft_limit))
        return False
    return True


def SubjectIsCapitalized(subject):
    line_format = re.compile(r"[a-zA-Z][a-z]*:\s[A-Z]")
    if not line_format.match(subject):
        print('The subject should be capitalized.')
        return False
    return True


def TextLengthIsValid(text_line):
    soft_limit = 72
    hard_limit = 80
    if len(text_line) > hard_limit:
        print("{}:Text line must be less than {} characters.".format(
            text_line, soft_limit))
        return False
    return True


def CommitFileIsValid(commit_file_name):
    with open(commit_file_name) as commit_file:

        subject_line = commit_file.readline()
        if SubjectIsValid(subject_line) is not True:
            print("Subject is not formatted correctly.  See .gitmessage.")
            return False

        label =  LabelFromSubject(subject_line)
        if LabelIsValid(label) is not True:
            print("Label for subject ({}) is not valid  See .gitmessage.".format(
                label))
            return False

        blank_line = commit_file.readline()
        if '\n' != blank_line:
            print("'{}'".format(blank_line))
            print("Seperate the subject from the body with a blank line.  "
                + "See .gitmessage.")
            return False

        for line in commit_file:
            if TextLengthIsValid(line) is not True:
                print(
                    "'{}'".format(line) +
                    "Lines in body text should be 72 characters or less.  "
                    + "See .gitmessage")
                return False
    return True


if __name__ == "__main__": # pragma: no cover
    if True == CommitFileIsValid(sys.argv[1]):
        exit(0)
    exit(1)
