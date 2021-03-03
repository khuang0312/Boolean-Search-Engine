from time import perf_counter

class Timer:
    def __init__(self, name : str):
        self.name = name                # describes what it is timing             
        self.begin = perf_counter()
        self.end = 0                    # 0 signifies if timer has stopped
    
    def __str__(self):
        return "Timer {}, {} seconds elapsed".format(self.name, self.time_elapsed())
    
    def __eq__(self, other):
        '''If a timer is timing the samething as another timer
        They are considered one and the same...
        '''
        return self.name == other.name

    def subject(self):
        '''Returns what the timer is timing
        '''
        return self.name
    
    def begin_and_end(self):
        '''Returns a tuple when timer started and when timer ended or current time
        '''
        return (self.begin, self.end if self.end != 0 else perf_counter())

    
    def has_stopped(self) -> bool:
        '''Timer only stops if the stop method has ben called...
        '''
        return self.end != 0

    def stop(self):
        '''Stops timer, the end time will be the time when
            this method is called
        '''
        self.end = perf_counter()
    
    def reset(self, name:str="new timer"):
        '''Reset timer such that start time is now the current time...
        '''
        self.name = name
        self.end = 0
        self.start = perf_counter()
    
    def time_elapsed(self) -> float:
        '''Returns fractional seconds
        '''
        if self.end == 0:
            return perf_counter() - self.begin
        return self.end - self.begin

def to_milliseconds(seconds):
    return seconds * 1000

        
if __name__ == "__main__":
    # create your timer
    # do whatever you need to do
    # stop timer
    # get timer properties as needed... 

    t = Timer("search1")
    # search1 code here
    t.stop()
    print(t)