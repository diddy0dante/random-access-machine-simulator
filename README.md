# random-access-machine-simulator
This is a simulator for a random-access machine (RAM), implemented in Python.

## Random-Access Machines
Not to be confused with Random Access _Memory_, a random-access machine is a conceptual register machine. You could think of it like an abstract computer that reads assembly-like language. You can read about them [on Wikipedia](https://en.wikipedia.org/wiki/Random-access_machine).

## This implementation
My Specific implementation has ten instructions, although seemingly too many. I found some very useful when I originally needed to make this. Any The instructions are as follows:
- `load i`: Load the value of register `i` into the CPU.
- `store i`: Store the value of the CPU into register `i`.
- `ldcpu`: "load cpu". dereference the address currently stored in the CPU and store it in the CPU.

- `add i`: Add `i` to the value of the CPU and store it in the CPU.
- `sub i`: Subtract `i` from the value of the CPU and store it in the CPU.

- `jump a`: Jump to flag `a` in the program.
- `jgtz a`: "jump greater than zero". Jump to flag `a` in the program if the value in the CPU is greater than zero.

- `halt`: Stop the program.

- `print s`: Print `s`. If `s` is an integer, it can be dereferenced.
- `pcpu`: "print cpu". Print the value of the CPU.
- `preg`: "print registers". Print the register file.

`load`, `store`, `add`, `sub`, and `print` support dereferencing their arguments with `*`. `ldcpu`, `halt`, and both prints are not required for Turing completeness. For elaboration on halt: the simulator stops automatically at the end of the program.

Any text behind a `#` is ignored, and any whitespace preceding and following an instruction is ignored, so code may be indented and commented with `#`. Furthermore, empty lines are also ignored.
