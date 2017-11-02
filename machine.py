def run(file):
    variables = {}
    
    def get(var):
        if(var.isdigit()):
            return int(var)
        return variables[var]
        
    def assing(var, value):
        variables[var] = get(value)
        return variables[var] 
    def invert(var):
        variables[var] = -variables[var]
        return variables[var]
    def increment(var):
        variables[var] += 1
        return variables[var]
    def translate(var, position):
        if(not (variables[var] == 0)):
            file.seek(0)
            for i in range(get(position)):
                file.readline()
    
    def interprete(statement):
        # statement es un arreglo donde:
        # s[0] = variable
        # s[1] = operacion
        # s[2] = valor (es opcional)
        
        var = statement[0]
        op = statement[1]
        
        if(op == '='):
            return assing(var, statement[2])
        elif(op == '+'):
            return increment(var)
        elif(op == '!'):
            return invert(var)
        elif(op == '->'):
            return translate(var, statement[2])
            
    def serialize(line):
        return line.split()
        
    for line in file:
        print(interprete(serialize(line)))

with open('sumator.mat', 'r') as file:
    run(file)