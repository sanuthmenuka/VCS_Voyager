# VCS_Voyager

An implementation of a version control system in python

## Git Objects

Everything(commits,blob,tree..etc) are stored as objects(files) in git. The contents of that file is the type of the object, the size and other info. The path and the filename of that object is computed by hash of contents inside the file.

cat-file prints contents of given object name with type
hash-object converts file to git object

kvlm parse method makes the format of the commit file
commits are only linked to the past. Only parents
