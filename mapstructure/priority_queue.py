class PriorityQueue(object):
    def __init__(self): 
        self.pre_init()

    def __init__(self, node_dict): 
        self.pre_init()
        for node in node_dict:
            self.push((node, node_dict[node][self.priority_index]))

    def pre_init(self):
        self.data_index = 0
        self.priority_index = 1
        self.queue = []

    def __str__(self): 
        return ' '.join([str(i) for i in self.queue]) 

    # for checking if the queue is empty 
    def isEmpty(self): 
        return len(self.queue) == []

    # for inserting an element in the queue 
    #This data should be an enum: (package, priority_integer)
    def push(self, data): 
        self.queue.append(data)

    def update(self, data):
        try: 
            for i in range(len(self.queue)):
                if self.queue[i][self.data_index] == data[self.data_index]:
                    del self.queue[i]
                    self.push(data)
                    return data #TODO: change return type if necessary
        except ValueError: 
            print() 
            exit() 


    # for popping an element based on Priority 
    def pop(self):
        try: 
            max = 0
            for i in range(len(self.queue)):
                if self.queue[i][self.priority_index] < self.queue[max][self.priority_index]:
                    max = i 
            item = self.queue[max] 
            del self.queue[max] 
            return item 
        except IndexError: 
            print() 
            exit() 