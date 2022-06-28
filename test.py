import os
import time


pid = os.fork()
r, w = os.pipe()

if pid == 0:
    os.dup2(r, 0)
    os.execlp("git", "pushing", "push", "--set-upstream", 'origin', 'master:demo')

pid2 = os.fork()
if pid2 == 0:
    os.write(w, b"goodnight-lab\x10")
    time.sleep(1)
    os.write(w, b"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\x10")
    exit()

os.wait()
