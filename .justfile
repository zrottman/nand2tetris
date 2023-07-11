list project ext:
    find projects/{{project}} | rg ".*{{ext}}$"

open project name ext:
    find projects/{{project}} -name {{name}}.{{ext}} -type f -exec vim {} \; -quit

test project chip:
    ./tools/HardwareSimulator.sh ./projects/{{project}}/{{chip}}.tst

debug project chip:
    ./tools/TextComparer.sh ./projects/{{project}}/{{chip}}.cmp ./projects/{{project}}/{{chip}}.out
    
testvm project name:
    # delete projects/07/../<name>.asm 
    find projects/{{project}}/ -name {{name}}.asm -type f -delete 2>/dev/null
    # translate all asm files
    find projects/{{project}}/ -name {{name}}.vm -type f -exec python3 projects/{{project}}/vmtranslator.py {} \;
    # test
    find projects/{{project}} -name {{name}}.tst -type f -exec ./tools/CPUEmulator.sh {} \;
