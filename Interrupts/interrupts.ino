#include <QueueList.h>
#include <StackArray.h>

//Declaring variables..
QueueList <int> low_pid;
StackArray <int> pid;
StackArray <int> timer;
int inPin1=7;
int inPin2=8;
int inPin3=9;
int val[5];
int current_pid=-1,temp_pid,curr_val=-1,temp_val;

//Returns the corresponding timer value..
int timers(int x)
{
  return 80-(x*10);
}

//Converts the input binary string to decimal..
int convert( int a[])
{
  int i,k=1,ans=0;
  for (i=2;i>=0;i--)
  {
    ans=ans+(k*a[i]);
    k=k*2;
  }
  return ans;
}



void setup() {
  Serial.begin(9600);
  pinMode(inPin1,INPUT);
  pinMode(inPin2,INPUT);
  pinMode(inPin3,INPUT);
}



void loop() {
  //Reading values from switches..
  val[0]=digitalRead(inPin1);
  val[1]=digitalRead(inPin2);
  val[2]=digitalRead(inPin3);

  //Converting the value..
  temp_pid=convert(val);

  //Finding the corresponding timer..
  temp_val=timers(temp_pid);

  //Base case..
  if (curr_val==-1 && current_pid==-1)
  {
    current_pid=temp_pid;
    curr_val=temp_val;
  }
  Serial.print("Process:");
  Serial.println(current_pid);
  Serial.print("Timer Value:");
  Serial.println(curr_val);

  //If a higher priority process comes in then stack the present process..
  if (temp_pid<current_pid)
  {
    pid.push(current_pid);
    timer.push(curr_val);
    current_pid=temp_pid;
    curr_val=temp_val;
    delay(1000);
    Serial.println("present process in stack");
  }

  //If a lower priority process comes in then queue it..
  else if (temp_pid>current_pid){
    
    if (curr_val>0){
    low_pid.push(temp_pid);
    Serial.println("new process in queue");
    curr_val--;
    delay(1000);
    }
    
    else{
      int x=pid.pop();
      if (x>temp_pid){

        
        
        
        current_pid=temp_pid;
        curr_val=timers(current_pid);
        timer.push(x);
        delay(1000);
      }
      
      else{
        low_pid.push(temp_pid);
        Serial.println("Queuing new process");
        curr_val=timer.pop();
        current_pid=x;
        delay(1000);
      }
      
    }
  }

  //Usual routine (No new interrupt comes in)..
  else{

    if (curr_val>0)
    {
      curr_val--;
      delay(1000);
    }
    
    else
    {
      if (timer.isEmpty()==false){
        current_pid=pid.pop();
        curr_val=timer.pop();
        delay(1000);
     }
     
     else{
      
        if (low_pid.isEmpty()==false){
          current_pid=low_pid.pop();
          Serial.print("Unstacking ");
          Serial.println(current_pid);
          curr_val=timers(current_pid);
          delay(1000);
        }
        
        if (timer.isEmpty()==true && low_pid.isEmpty()==true){
        Serial.println("No Intterupt");
        delay(1000);
        }
        
      }
      
    }
  }
  }

