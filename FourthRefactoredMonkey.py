import random

sigmoid = lambda x: 1/(1+pow(2.7128,-x))
tanh = lambda x: (pow(2.7128,x)-pow(2.7128,-x))/(pow(2.7128,x)+pow(2.7128,-x))

def dot(X,Y):
        try:
            return [[sum(a*b for a,b in zip(X_row,Y_col)) for Y_col in zip(*Y)] for X_row in X]
        except:
            raise Exception("Wrong Matrix Shape")
        
def add(X,Y):
    return[[a+b for a,b in zip(x,y)] for x,y in zip(X,Y)]

def random_matrix(a,b):
    return [[random.random()*random.choice([1,-1]) for i in range(b)] for j in range(a)]

def random_matrix(a,b):
    return [[random.random() for i in range(b)] for j in range(a)]

sigmoid = lambda x: 1/(1+(2.7182818284**(float(-x))))
sigmoid_matrix = lambda x: [[sigmoid(y)for y in j]for j in x]

class n_layer:
    def __init__(self,a,b):
        self.i_l = a
        self.o_l = b  
        self.weights = random_matrix(self.o_l,self.i_l)
        self.bias = random_matrix(self.o_l,1)
    def activate(self,m):
        self.m = m
        self.z = add(dot(self.weights,self.m),self.bias)
        self.pred = sigmoid_matrix(self.z)

class neural_net:
    def __init__(self,dim):
        self.dim = dim
        self.brain = []
        self.score = None
        for i in range(len(dim)-1):
            self.brain.append(n_layer(dim[i],dim[i+1]))
            
    def activate(self,m):
        self.brain[0].activate(m)
        for i in range(1,len(self.brain)):
            self.brain[i].activate(self.brain[i-1].pred)
        self.pred = self.brain[-1].pred
        self.z = sigmoid_matrix(self.brain[-1].z)
        

def mutate(a):
    for i in range(len(a.brain)):
        for j in range(len(a.brain[i].weights)):
            for k in range(len(a.brain[i].weights[j])):
                chooser = random.random()
                if chooser > 0.85:
                    a.brain[i].weights[j][k] = random.random()*random.choice([1,-1])

def reproduce(a,b):
    c = n_layer(a.i_l,a.o_l)
    for i in range(len(a.weights)):
        for j in range(len(a.weights[i])):
            c.weights[i][j] = random.choice([a.weights[i][j],b.weights[i][j]])
    return c

def mate(a,b):
    c = neural_net(a.dim)
    for i in range(len(c.brain)):
        c.brain[i] = reproduce(a.brain[i],b.brain[i])
    mutate(c)
    return c

def otherin(list,item):
    for i in list:
        if i == item:
            return True
    return False

def otherind(list,item):
    for i in list:
        if i == item:
            return i
    return False

class Connection_Gene:
    def __init__(self, input, output, ancestry, weight = None, disabled = None):
        self.weight = random.random()*random.choice([-1,1]) if weight == None else weight
        self.output_node = output
        self.input_node = input
        self.disabled = False if disabled == None or disabled == False else True
        self.innov = None
        self.input,self.output = input.index,output.index
        self.address = str(input)+str(output)

        self.assign_innov(ancestry)

    def __eq__(self,other):
        if self.input == other.input and self.output == other.output:
            return True
        return False
    
    def assign_innov(self,ancestry):
        for i in ancestry:
            if i[0] == self:
                self.innov = i[0].innov
                return 1
        ancestry.append([self,len(ancestry)])
        self.innov = len(ancestry)
        return 0

class Node_Gene:
    def __init__(self,mode,index):
        self.mode = mode
        self.input = []
        self.genes = []
        self.index = index
        self.pred = None

    def __eq__(self,other):
        return self.mode == other.mode and self.index == other.index and self.input == other.input

    def set_io(self,genes):
        '''NOTE: THE GENES AND INPUT INDEXES ARE STORED IDENTICALLY, 
                 KEEP THIS IN MIND FOR FURTHER ADDITIONS'''
        for i in genes:
            if self.index == i.output:
                self.input.append(i.input_node)
                self.genes.append(i)

    def activate(self,input=None):
        if self.mode == "I":
            if input == None:
                raise Exception("No input for input node")
            self.pred = input
        else:
            self.pred = 0
            for i in range(len(self.input)):
                self.pred+=self.input[i].pred*self.genes[i].weight
            self.pred = tanh(self.pred)

class Network:
    def __init__(self,input,output,innov):
        self.Nodes = [[],[],[]]
        self.Genes = []

        self.index = 0
        self.pred = []

        self.fitness = None 

        for i in range(input):
            self.Nodes[0].append(Node_Gene("I",self.index))
            self.index += 1
        for i in range(output):
            self.Nodes[2].append(Node_Gene("O",self.index))
            self.index+=1
        
        # for i in self.Nodes[0]:
        #     for j in self.Nodes[2]:
        #          self.Genes.append(Connection_Gene(i.index,j.index,innov))
            
        for i in self.Nodes[2]:
            i.set_io(self.Genes)

        
    def activate(self,input):
        for i in range(len(input)):
            self.Nodes[0][i].activate(input[i])
        for i in self.Nodes[1]:
            i.activate()
        for i in self.Nodes[2]:
            i.activate()
            self.pred.append(i.pred)

    def mutate_weights(self,threshold = 0.9):
        for i in self.Genes:
            chooser = random.random()
            if chooser>threshold:
                i.weight = random.random()*random.choice([-1,1])

    def add_connection(self,innov): 
        ochooser = [i for i in self.Nodes[2]]
        checker = False
        if len(self.Nodes[1]) != 0:
            for i in self.Nodes[1]:
                ochooser.append(i)
                checker = True
        messiah = random.random()
        if messiah > 0.5:
            newcon = Connection_Gene(random.choice(self.Nodes[0]),random.choice(ochooser),innov)
        else:
            if checker:
                first = random.choice(self.Nodes[1])
                newcon = Connection_Gene(first,random.choice(ochooser.remove(first)),innov)
            else:
                newcon = Connection_Gene(random.choice(self.Nodes[0]),random.choice(ochooser),innov)

 
        self.Genes.append(newcon)
        for i in self.Nodes[2]:  
            i.set_io(self.Genes)
        for i in self.Nodes[1]:
            i.set_io(self.Genes)

    def add_node(self,innov):
        number = random.randint(0,len(self.Genes)-1)
        self.Genes[number].disabled = False
        self.Nodes[1].append(Node_Gene("H",self.index))
        self.index+=1
        self.Genes.append(Connection_Gene(self.Genes[number].input_node,self.Nodes[1][-1],innov))
        self.Genes.append(Connection_Gene(self.Nodes[1][-1],self.Genes[number].output_node,innov))
        self.Nodes[1][-1].set_io(self.Genes)

    def set_species(self,specie):
        self.specie = specie

def calc_similarity(NN1,NN2,m_co=0.5,w_co = 0.1):
    first = sorted(NN1.Genes,key=lambda x: x.innov)
    second = sorted(NN2.Genes,key=lambda x: x.innov)

    un_match = 0
    match = 0

    wavg  = []

    for i in range(min(len(first),len(second))):
        if(first[i] == second[i]):
            wavg.append(abs(first[i].weight-second[i].weight))
            match+=1
        else:
            un_match+=1
    
    un_match+=max(len(first),len(second))-min(len(first),len(second))
    wav = sum(wavg)/len(wavg) if len(wavg)>0 else 0
    N = max(len(first),len(second))

    thresher = ((m_co*un_match)/N)+(w_co*wav)
    return thresher

def reproducer(NN1,NN2,innov):
    first = sorted(NN1.Genes,key = lambda x: x.innov)
    second = sorted(NN2.Genes,key = lambda x: x.innov)

    fitter = first if NN1.fitness > NN2.fitness else second

    new = []
    newNodes = []

    for i in range(min(len(first),len(second))):
        if first[i] == second[i]:
            new.append(random.choice([first[i],second[i]]))
        else:
            new.append(fitter[i])
    
    for i in range(min(len(first),len(second)),len(fitter)):
        new.append(fitter[i])
    nndex = 0 
    for i in new:
        if not otherin(newNodes,i.output_node):
            if i.output_node.mode == "H":
                newNodes.append(i.output_node)
                nndex+=1
            if i.output_node.mode == "I":
                newNodes.append(i.output_node)
                nndex+=1
            if i.output_node.mode == "O":
                newNodes.append(i.output_node)
                nndex+=1
        if not otherin(newNodes,i.input_node):
            if i.input_node.mode == "H":
                newNodes.append(i.input_node)
                nndex+=1
            if i.input_node.mode == "I":
                newNodes.append(i.input_node)
                nndex+=1
            if i.input_node.mode == "O":
                newNodes.append(i.input_node)
                nndex+=1

    ref = [[],[],[]]

    for i in newNodes:
        if i.mode == "O":
            ref[2].append(i)
        if i.mode == "H":
            ref[1].append(i)
        if i.mode == "I":
            ref[0].append(i)
    
    newNodes = ref
    newN = Network(1,1,innov)

    newN.Nodes = newNodes
    newN.Genes = new
    newN.index = nndex

    for i in newN.Nodes[1]:
        i.set_io(newN.Genes)
    for i in newN.Nodes[2]:
        i.set_io(newN.Genes)
    try:
        newN.activate([1 for i in newN.Nodes[0]])
    except:
        return reproduce(NN1,NN2,innov)
    return newN

def handlespecies(networks, species, threshold=0.5):
    for net_group in networks:
        for net in net_group:
            found_species = False
            for specie in species:
                if calc_similarity(net, specie[0]) < threshold:
                    specie.append(net)
                    net.set_species(specie)
                    found_species = True
                    break
            
            if not found_species:
                new_species = [net]
                species.append(new_species)
                net.set_species(new_species)

def print_network(NN):
    for i in NN.Genes:
        print([i.input,i.output,i.disabled])
        print(i.weight)  
    print(NN.Nodes)  


