import os


pid = os.fork()

if pid == 0:
    import sys
    r, w = os.pipe()
    os.dup2(r, 0)
    os.close(r)
    os.write(w, b"GoodDay-lab\x10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\x10")
    os.execlp("git", "pushing", "push", "--set-upstream", 'origin', 'demo')
os.wait()
