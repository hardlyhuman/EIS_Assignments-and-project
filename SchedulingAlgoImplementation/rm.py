import string
import random
from prime import lcm


class task(object):

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

#Task types (templates for periodic tasks)
class tasktype(object):

    def __init__(self, period, release, execution, deadline, name):
        self.period    = period
        self.release   = release
        self.execution = execution
        self.name      = name

#Priority comparison
def priority_cmp(one, other):
    if one.priority < other.priority:
        return -1
    elif one.priority > other.priority:
        return 1
    return 0

#Rate monotonic comparison
def tasktype_cmp(self, other):
    if self.period < other.period:
        return -1
    if self.period > other.period:
        return 1
    return 0

if __name__ == '__main__':
    u=0.000
    taskfile = open('tasks.txt')
    lines = taskfile.readlines()
    task_types = []
    tasks = []
    hyperperiod = []
    html_color = { 'Task1':'red', 'Task2':'blue', 'Task3':'green', 'Task4':'aqua', 'Task5':'coral', 'Empty':'grey', 'Finish':'black'}
    #Allocate task types
    for line in lines:
        line = line.split(' ')  
        for i in range (0,3):
            line[i] = int(line[i])
        u+=float(line[2])/float(line[0])
        print "Utilisation Factor:" + str(u)
            #print line[i]
            #print
        if len(line) == 4:
            name = line[3]
        elif len(line) == 3:
            name = 'Task'
        else:
            raise Exception('Invalid tasks.txt file structure')
        if int(line[0])>0:
            task_types.append(tasktype(period=line[0], release=line[1], execution=line[2], deadline=line[3], name=name))
        
    #Calculate hyperperiod
    for task_type in task_types:
        hyperperiod.append(task_type.period)
    hyperperiod = lcm(hyperperiod)

    #Sort
    task_types = sorted(task_types, tasktype_cmp)


    #Create new task instances 
    for i in xrange(0, hyperperiod):
        for task_type in task_types:
            if  (i - task_type.release) % task_type.period == 0 and i >= task_type.release:
                start = i
                end = start + task_type.execution
                priority = task_type.period
                tasks.append(task(start=start, end=end, priority=priority, name=task_type.name))

    html = "<!DOCTYPE html><html><head><title>Rate Monotonic Scheduling</title></head><body>"

    utilization = 0
    for task_type in task_types:
        utilization += float(task_type.execution) / float(task_type.period)
    if utilization > 1:
        print 'Not Schedulable!'
        html += '<br /><br />Not Schedulable<br /><br />'

    #clock
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
                print "Executed!" ,
        else:
            print 'No task uses the processor. '
            html += '<div style="float: left; text-align: center; width: 110px; height: 20px; background-color:' + html_color['Empty'] + ';">Empty</div>'
        print "\n"

    #Print remaining periodic tasks
    html += "<br /><br />"
    for p in tasks:
        print p.get_unique_name() + " failed execution"
        html += "<p>" + p.get_unique_name() + " Failed Execution</p>"

    html += "</body></html>"
    output = open('output.html', 'w')
    output.write(html)
    output.close()
