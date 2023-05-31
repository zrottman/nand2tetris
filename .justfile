list project:
    find projects/{{project}} | rg ".*(hdl|asm)"

open project chip:
    vim ./projects/{{project}}/{{chip}}.hdl
