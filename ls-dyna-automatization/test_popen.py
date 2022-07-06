import subprocess

p = subprocess.Popen(["powershell", ""])
"""
A None value indicates that the process hasn't terminated yet.
"""
poll = p.poll()
if poll is None:
  print("Yes")
  print(poll)
else:
  print("No")