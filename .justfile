list project:
    find projects/{{project}} | rg ".*(hdl|asm)"

open project chip:
    vim ./projects/{{project}}/{{chip}}.hdl

test project chip:
    ./tools/HardwareSimulator.sh ./projects/{{project}}/{{chip}}.tst

debug project chip:
    ./tools/TextComparer.sh ./projects/{{project}}/{{chip}}.cmp ./projects/{{project}}/{{chip}}.out
