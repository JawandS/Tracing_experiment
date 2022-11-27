# Analyzing CPU Consumption
### TensorFlow Analysis using bpftrace 
##

## Execution  
Execute run.sh for data collection on mdoel.py:  
bpftrace -e 'tracepoint:sched:sched_switch { printf("%s %lu %d %lu\n", comm, pid, cpu, nsecs); }'

- Using bpftrace to trace context switches
- model.py is a TensorFlow deep learning job that automatically kills tracing
- The timeline is analyzed with processing.py
- fib.py is a fibonacci job (does not kill tracing)
- Pass run number to run.sh for