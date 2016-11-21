import difflib

text1 = """This is line 1
this line differs
this line is same"""
text1_lines = text1.splitlines()

text2 = """This is line 1
this line defers :P
this line is same
this is an extra line"""
text2_lines = text2.splitlines()


d = difflib.Differ()
diff = d.compare(text1_lines, text2_lines)
print '\n'.join(diff)