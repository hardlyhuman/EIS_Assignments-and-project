import string
import random
from prime import lcm

class TaskIns(object):

    
    def __init__(self, start, end, priority, name):
        self.start    = start
        self.end      = end
        self.usage    = 0
        self.priority = priority
        self.name     = name.replace("\n", "")
        self.id = int(random.random() * 10000)

    def use(self, usage):
        self.usage += usage
        if self.usage >= self.end - self.start:
            return True
        return False
    
  
   def __repr__(self):
        return str(self.name) + "#" + str(self.id) + " - start: " + str(self.start) + " priority: " + str(self.priority) + budget_text

    
    def get_unique_name(self):
        return str(self.name)


class TaskType(object):

    def __init__(self, period, release, execution, deadline, name):
        self.period    = period
        self.release   = release
        self.execution = execution
        self.deadline  = deadline
        self.name      = name

#Priority comparison
def priority_cmp(one, other):
    if one.priority < other.priority:
        return -1
    elif one.priority > other.priority:
        return 1
    return 0

#Deadline monotonic comparison
def tasktype_cmp(self, other):
    if self.deadline < other.deadline:
        return -1
    if self.deadline > other.deadline:
        return 1
    return 0

if __name__ == '__main__':
    #Variables
    u=0.000
    html_color = { 'Task1':'red', 'Task2':'blue', 'Task3':'green', 'Task4':'aqua', 'Task5':'coral', 'Empty':'grey', 'Finish':'black'}
    taskfile = open('task.txt')
    lines = taskfile.readlines()
    task_types = []
    tasks = []
    hyperperiod = []

    #Allocate task types
    for line in lines:
        line = line.split(' ')  
        for i in range (0,4):
            line[i] = int(line[i])
        u+=float(line[2])/float(line[0])
        print "Utilisation Factor:" + str(u)
        if len(line) == 5:
            name = line[4]
        
        elif len(line) == 4:
            name = 'Task'
        else:
            raise Exception('Invalid tasks.txt file structure')
        if int(line[0])>0:
            task_types.append(TaskType(period=line[0], release=line[1], execution=line[2], deadline=line[3], name=name))
        
    #Calculate hyperperiod
    for task_type in task_types:
        hyperperiod.append(task_type.period)
    hyperperiod = lcm(hyperperiod)

    #Sort types rate monotonic
    task_types = sorted(task_types, tasktype_cmp)


    #Create task instances 
    for i in xrange(0, hyperperiod):
        for task_type in task_types:
            if  (i - task_type.release) % task_type.period == 0 and i >= task_type.release:
                start = i
                end = start + task_type.execution
                priority = start + task_type.deadline
                tasks.append(TaskIns(start=start, end=end, priority=priority, name=task_type.name))

    #Html output start
    html = "<!DOCTYPE html><html><head><title>EDF Scheduling</title></head><body>"

    #Check utilization
    utilization = 0
    for task_type in task_types:
        utilization += float(task_type.execution) / float(task_type.period)
    if utilization > 1:
        print 'Not Schedulable'
        html += '<br/>Not Schedulable!<br />'

    #Simulate clock
    clock_step = 1
    for i in xrange(0, hyperperiod, clock_step):
        
        possible = []
        for t in tasks:
            if t.start <= i:
                possible.append(t)
        possible = sorted(possible, priority_cmp)

        #Select task with highest priority
        if len(possible) > 0:
            on_cpu = possible[0]
            print on_cpu.get_unique_name() , " uses the processor. " , 
            html += '<div style="float: left; text-align: center; width: 110px; height: 20px; background-color:' + html_color[on_cpu.name] + ';">' + on_cpu.get_unique_name() + '</div>'
            if on_cpu.use(clock_step):
                tasks.remove(on_cpu)
                html += '<div style="float: left; text-align: center; width: 10px; height: 20px; background-color:' + html_color['Finish'] + ';"></div>'
                print "Finish!" ,
        else:
            print 'No task uses the processor. '
            html += '<div style="float: left; text-align: center; width: 110px; height: 20px; background-color:' + html_color['Empty'] + ';">Empty</div>'
        print "\n"

    #Print remaining periodic tasks
    html += "<br /><br />"
    for p in tasks:
        print p.get_unique_name() + " is dropped due to overload!"
        html += "<p>" + p.get_unique_name() + " is dropped due to overload!</p>"

    #Html output end
    html += "</body></html>"
    output = open('output.html', 'w')
    output.write(html)
    output.close()