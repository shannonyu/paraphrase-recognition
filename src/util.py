#!/usr/bin/python

def is_alphabet(line):
	if len(line) != 1:
		return False

	if 'a' <= line and line <= 'z':
		return True

	if 'A' <= line and line <= 'Z':
		return True

	return False
