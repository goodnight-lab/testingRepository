import os


pid = os.fork()

if pid == 0:
    import sys
    r, w = os.pipe()
    os.dup2(r, 0)
    os.close(r)
    os.write(w, b"goodnight-lab\x10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\x10")
    print("23")
    os.execlp("git", "pushing", "push", "--set-upstream", 'origin', 'demo')
os.wait()
