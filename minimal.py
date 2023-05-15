import copy


class dfa_node:
    def __init__(self, name):
        self.name = name
        self.next = {}

    def printOut(self):
        print(self.name)
        print(self.next)



states = []

f = open("minimal.in", "r")

states_count = int(f.readline().split(" ")[0])

for i in range(states_count):
    states.append(dfa_node('q' + str(i)))

initial_state = f.readline().split(" ")[0][1]

lines = f.readlines()

final_states = [int(x[1]) for x in lines[0].split(" ")]


for line in lines[1:]:
    line = line.strip().split(" ")
    states[int(line[0][1])].next[line[1]] = line[2]
    

transitions = list(states[0].next.keys())

initial_partitions = [[x for x in range(states_count) if x not in final_states], final_states]



def same_partition(state1, state2, partitions):
    for partition in partitions:
        if state1 in partition and state2 in partition:
            return 1
    return 0


def partitioner(partitions, states, transitions):
    new_partitions = []
    copy_partitions = copy.deepcopy(partitions)
    k = 0
    
    for i in range(len(partitions)):
        s1 = 0
        
        while s1 < len(partitions[i]):
            state1 = partitions[i][s1]
            new_partitions.append([])
            new_partitions[k].append(state1)
            s2 = s1 + 1
            
            while s2 < len(partitions[i]):
                state2 = partitions[i][s2]
                ok = 1
                
                for transition in transitions:
                    tr1 = int(states[state1].next[transition][1])
                    tr2 = int(states[state2].next[transition][1])
                    if not same_partition(tr1, tr2, copy_partitions):
                        ok = 0
                        
                if ok == 1:
                    new_partitions[k].append(state2)
                    partitions[i].remove(state2)
                    s2 -= 1
                s2 += 1
            s1 += 1
            k += 1
            
    if copy_partitions != new_partitions:
        copy_partitions = new_partitions
        return partitioner(new_partitions, states, transitions)
    else:
        return copy_partitions


partitions = partitioner(initial_partitions, states, transitions)


def buildNewStates(state, partitions):
    for new_state in partitions:
        if state in new_state:
            return 'q' + "".join([str(x) for x in new_state])
        


def build_dfa(partitions, states, initial_state, final_states):
    new_states = []
    new_initial_state = ''
    new_final_states = set([])
    k = 0
    
    for state in partitions:
        name = "".join([str(x) for x in state])
        new_states.append(dfa_node('q' + name))
        
        for transition in transitions:
            new_next = buildNewStates(int(states[state[0]].next[transition][1]), partitions)
            new_states[k].next[transition] = new_next
            
        k += 1
        
        new_initial_state = buildNewStates(int(initial_state), partitions)
        
        for s in final_states:
            new_final_states.add(buildNewStates(s, partitions))
            
            
    return new_states, new_initial_state, new_final_states



new_states, new_initial_state, new_final_states = build_dfa(partitions, states, initial_state, final_states)



print("DFA Minimizat:")
for state in new_states:
    state.printOut()
    
print("Starea initiala noua", new_initial_state)
print("Starea finala noua", *new_final_states)
print()

