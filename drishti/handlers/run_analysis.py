#!/usr/bin/env python3
import sys
from template import DrishtiAnalysis
from unified_handler import handler as drishti_counter

def get_analysis(log_path):

    # Create a fake args object for the handler.
    class ArgsFake:
        pass
    args_fake = ArgsFake()
    args_fake.log_path = log_path
    args_fake.backtrace = False
    args_fake.split_files = False

    global args
    args = args_fake

    drishti_counters = drishti_counter(args_fake)

    # Load the counters into a DrishtiAnalysis instance.
    analysis = DrishtiAnalysis()
    for key, value in drishti_counters.items():
        try:
            analysis.set_counter(key, value)
        except KeyError:
            pass

    return analysis

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_analysis.py /path/to/file.darshan")
        sys.exit(1)
    log_file = sys.argv[1]
    analysis = get_analysis(log_file)
    
    print("Total Write Size STDIO:", analysis.get_counter("total_write_size_stdio"))
    print("Total Read Size STDIO:", analysis.get_counter("total_read_size_stdio"))
    print("Total Size STDIO:", analysis.get_counter("total_size_stdio"))
    print("Total Write Size POSIX:", analysis.get_counter("total_write_size_posix"))
    print("Total Read Size POSIX:", analysis.get_counter("total_read_size_posix"))
    print("Total Size POSIX:", analysis.get_counter("total_size_posix"))
    print("Total Write Size MPI-IO:", analysis.get_counter("total_write_size_mpiio"))
    print("Total Read Size MPI-IO:", analysis.get_counter("total_read_size_mpiio"))
    print("Total Size MPI-IO:", analysis.get_counter("total_size_mpiio"))
    print("Total Size:", analysis.get_counter("total_size"))
    print("Total Reads:", analysis.get_counter("total_reads"))
    print("Total Writes:", analysis.get_counter("total_writes"))
    print("Total Operations:", analysis.get_counter("total_operations"))
    print("Total Read Size:", analysis.get_counter("total_read_size"))
    print("Total Written Size:", analysis.get_counter("total_written_size"))
    print("Total Reads Small:", analysis.get_counter("total_reads_small"))
    print("Total Writes Small:", analysis.get_counter("total_writes_small"))
    print("Total Mem Not Aligned:", analysis.get_counter("total_mem_not_aligned"))
    print("Total File Not Aligned:", analysis.get_counter("total_file_not_aligned"))
    print("Max Read Offset:", analysis.get_counter("max_read_offset"))
    print("Max Write Offset:", analysis.get_counter("max_write_offset"))
    print("Read Consecutive:", analysis.get_counter("read_consecutive"))
    print("Read Sequential:", analysis.get_counter("read_sequential"))
    print("Read Random:", analysis.get_counter("read_random"))
    print("Write Consecutive:", analysis.get_counter("write_consecutive"))
    print("Write Sequential:", analysis.get_counter("write_sequential"))
    print("Write Random:", analysis.get_counter("write_random"))
    print("Total Shared Reads:", analysis.get_counter("total_shared_reads"))
    print("Total Shared Reads Small:", analysis.get_counter("total_shared_reads_small"))
    print("Total Shared Writes:", analysis.get_counter("total_shared_writes"))
    print("Total Shared Writes Small:", analysis.get_counter("total_shared_writes_small"))
    print("Total Transfer Size:", analysis.get_counter("total_transfer_size"))
    print("Total Transfer Time:", analysis.get_counter("total_transfer_time"))
    print("MPI-IO Coll Reads:", analysis.get_counter("mpiio_coll_reads"))
    print("MPI-IO Indep Reads:", analysis.get_counter("mpiio_indep_reads"))
    print("Total MPI-IO Read Ops:", analysis.get_counter("total_mpiio_read_operations"))
    print("MPI-IO Coll Writes:", analysis.get_counter("mpiio_coll_writes"))
    print("MPI-IO Indep Writes:", analysis.get_counter("mpiio_indep_writes"))
    print("Total MPI-IO Write Ops:", analysis.get_counter("total_mpiio_write_operations"))
    print("MPI-IO Non-blocking Reads:", analysis.get_counter("mpiio_nb_reads"))
    print("MPI-IO Non-blocking Writes:", analysis.get_counter("mpiio_nb_writes"))

if __name__ == "__main__":
    main()
