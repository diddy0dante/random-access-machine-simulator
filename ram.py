# Notes:
# My implementation by default uses add and sub instructions that take
# immediate values. This is because I use # for comments, and I saw nothing
# illogical about using immediate values by default and dereferencing them
# with *.

class RAM:

    def __init__(self, program, inp):
        self.jump_flags = {}
        self.reg_file = []
        self.program = []
        self.load_instructions(program)
        self.load_memory(inp)
        self.cpu = 0
        self.program_counter = 0
        self.finished = False

    def load_instructions(self, program):
        self.program = []
        for line in program:

            # Parse input
            line = line.split('#')[0].strip()
            if line == '':
                continue
            try:
                instr_s, arg_s = line.split(' ')
            except ValueError:
                instr_s = line
                arg_s = '0'

            # Map input instructions to functions
            instr_dict = {
                'load':  self.load,  'ldcp': self.ldcp, 'store': self.store,
                'add':   self.add,   'sub':  self.sub,  'halt':  self.halt,
                'jump':  self.jump,  'jgtz': self.jgtz,
                'print': self.print, 'pcpu': self.pcpu
            }
            instr_s = instr_s.lower()
            if instr_s[-1] == ':':
                self.jump_flags[instr_s[:-1]] = len(self.program)-1
                continue
            else:
                instr = instr_dict[instr_s]

            # Count dereferences
            arg = arg_s.replace('*', '')
            if arg.isnumeric():
                arg = int(arg)
            refs = 0
            for i in arg_s:
                if i == '*':
                    refs += 1
                else:
                    break

            # Commit
            self.program.append((instr, arg, refs))

    def load_memory(self, inp):
        self.reg_file = []
        for reg in inp:
            self.reg_file.append(int(reg))

    def execute(self):
        while self.finished == False:
            self.step()

    def step(self):
        instr, arg, refs = self.program[self.program_counter]
        while True:
            try:
                instr(arg, refs)
                break
            except IndexError:
                # Add more registers if neccesary. (Lazy approach but it works)
                self.reg_file.append(0)
        self.program_counter += 1
        if self.program_counter == len(self.program):
            self.finished = True

    def deref(self, i, n):
        for _ in range(n):
            i = self.reg_file[i]
        return i

    # From here on instructions

    def load(self, i, n):
        self.cpu = self.reg_file[self.deref(i, n)]

    def ldcp(self, *_):
        self.cpu = self.reg_file[self.cpu]

    def store(self, i, n):
        self.reg_file[self.deref(i, n)] = self.cpu

    def add(self, i, n):
        self.cpu += self.deref(i, n)

    def sub(self, i, n):
        self.cpu -= self.deref(i, n)

    def halt(self, *_):
        self.finished = True

    def jump(self, a, _):
        self.program_counter = self.jump_flags[a]

    def jgtz(self, a, _):
        if self.cpu > 0:
            self.program_counter = self.jump_flags[a]

    def print(self, s, n):
        if isinstance(s, int):
            print(self.deref(s, n))
        else:
            print(s)

    def pcpu(self, *_):
        print(self.cpu)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print('bad args', file=sys.stderr)
        exit(1)

    program_f = open(sys.argv[1])
    input_f = open(sys.argv[2])

    ram = RAM(program_f, input_f)
    ram.execute()

    print(ram.reg_file)
