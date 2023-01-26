import os
 
vad_files = set()
dfy_files = set()

# os.system("make clean && make verified -j8")

for r, d, f in os.walk("verified"):
    for file in f:
        path = os.path.join(r, file)
        if file.endswith(".verified"):
            os.system(f"rm {path}")
        elif file.endswith('.dfy'):
            dfy_files.add(path)
        elif file.endswith(".vad"):
            vad_files.add(path)

for f in vad_files:
    gdfy = f.replace(".vad", ".gen.dfy")
    # make sure all vad files are generated
    assert (gdfy in dfy_files)

print("""
rule dafny
    command = tools/dafny/Dafny.exe $flags $in && touch $out

rule dafny-nl
    command = tools/dafny/Dafny.exe $flags $in && touch $out
""")

flags = {
    "bit-vector-lemmas.i": "/proverOpt:OPTIMIZE_FOR_BV=true",
    "bitvectors.s" :" /proverOpt:OPTIMIZE_FOR_BV=true",
    "bitvectors_primitive.i": "/proverOpt:OPTIMIZE_FOR_BV=true",
    "bitvectors.i": "/proverOpt:OPTIMIZE_FOR_BV=true",
    "ptebits.i": "/proverOpt:OPTIMIZE_FOR_BV=true",
    "psrbits.i": "/proverOpt:OPTIMIZE_FOR_BV=true",
    "entrybits.i": "/proverOpt:OPTIMIZE_FOR_BV=true"}

DEFAULT_FLAGS = "/timeLimit:90 /ironDafny /allocated:1 /induction:1 /proverLog:@FILE@@PROC@.smt2 /compile:0"
for dfy_path in dfy_files:
    cur_flags = DEFAULT_FLAGS
    for name, fg in flags.items():
        if name in dfy_path:
            cur_flags += " " + fg
    if "nlarith." in dfy_path:
        print(f"build {dfy_path}.verified : dafny-nl {dfy_path}")
        print(f"  flags = {cur_flags}")
    else:
        cur_flags += " /noNLarith"
        print(f"build {dfy_path}.verified : dafny {dfy_path}")
        print(f"  flags = {cur_flags}")
    print("")