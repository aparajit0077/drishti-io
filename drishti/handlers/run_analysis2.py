#!/usr/bin/env python3
import sys
import os
import datetime
from types import SimpleNamespace
import pandas as pd

import drishti.includes.module as di_module
from drishti.includes.config import insights_total, insights_operation, insights_metadata, thresholds, HIGH, WARN, RECOMMENDATIONS, OK

def patched_display_footer(console, start, end):
    """
    If 'end' is a float (elapsed seconds), convert it to a datetime by adding it to 'start'.
    Then print a custom message with the total elapsed seconds.
    """
    if isinstance(start, datetime.datetime) and not isinstance(end, datetime.datetime):
        elapsed_seconds = float(end)
        end = start + datetime.timedelta(seconds=elapsed_seconds)
    total_seconds = (end - start).total_seconds()
    console.print(f"[green]Drishti: finished in {total_seconds:.2f} seconds.[/green]")
    return console

# Override the original display_footer
di_module.display_footer = patched_display_footer

from unified_handler import handler as drishti_counter , determine_trace_type

from template import DrishtiAnalysis

from drishti.includes.module import (
    init_console,
    display_content,
    display_thresholds,
    export_html,
    check_stdio,
    check_mpiio,
    check_operation_intensive,
    check_size_intensive,
    check_small_operation,
    check_misaligned,
    check_traffic,
    check_random_operation,
    check_shared_small_operation,
    check_long_metadata,
    check_shared_data_imblance_split,
    check_shared_data_imblance,
    check_shared_time_imbalance_split,
    check_shared_time_imbalance,
    check_individual_write_imbalance_split,
    check_individual_read_imbalance_split,
    check_individual_write_imbalance,
    check_individual_read_imbalance,
    check_mpi_collective_read_operation,
    check_mpi_collective_write_operation,
    check_mpi_none_block_operation,
    check_mpi_aggregator,
    insights_total,
    insights_metadata,
    HIGH,
    WARN,
    RECOMMENDATIONS,
)

from handle_darshan import display_drishti_output as display_drishti_output_darshan
from handle_recorder import display_drishti_output as display_drishti_output_recorder  

console = init_console()
def get_analysis(log_path):
    class ArgsFake:
        pass
    args_fake = ArgsFake()
    args_fake.log_path = log_path
    args_fake.backtrace = True
    args_fake.split_files = False

    drishti_counters = drishti_counter(args_fake)

    analysis = DrishtiAnalysis()
    for key, value in drishti_counters.items():
        try:
            analysis.set_counter(key, value)
        except KeyError:
            pass

    return analysis

def main():
    if len(sys.argv) < 2:
        print("Usage: run_analysis2.py /path/to/log")
        sys.exit(1)
    log_path = sys.argv[1]

    trace_type = determine_trace_type(log_path)
    if trace_type is None:
        print("Invalid log path provided. Must be either a file or a directory.")
        sys.exit(1)

    # Get DrishtiAnalysis instance with counters.
    analysis = get_analysis(log_path)

    total_size             = analysis.get_counter("total_size") or 0
    total_size_stdio       = analysis.get_counter("total_size_stdio") or 0
    total_size_posix       = analysis.get_counter("total_size_posix") or 0
    total_size_mpiio       = analysis.get_counter("total_size_mpiio") or 0
    total_reads            = analysis.get_counter("total_reads") or 0
    total_writes           = analysis.get_counter("total_writes") or 0
    total_operations       = analysis.get_counter("total_operations") or 0
    total_read_size        = analysis.get_counter("total_read_size") or 0
    total_written_size     = analysis.get_counter("total_written_size") or 0
    total_reads_small      = analysis.get_counter("total_reads_small") or 0
    total_writes_small     = analysis.get_counter("total_writes_small") or 0
    total_mem_not_aligned  = analysis.get_counter("total_mem_not_aligned") or 0
    total_file_not_aligned = analysis.get_counter("total_file_not_aligned") or 0
    max_read_offset        = analysis.get_counter("max_read_offset") or 0
    max_write_offset       = analysis.get_counter("max_write_offset") or 0
    read_consecutive       = analysis.get_counter("read_consecutive") or 0
    read_sequential        = analysis.get_counter("read_sequential") or 0
    read_random            = analysis.get_counter("read_random") or 0
    write_consecutive      = analysis.get_counter("write_consecutive") or 0
    write_sequential       = analysis.get_counter("write_sequential") or 0
    write_random           = analysis.get_counter("write_random") or 0
    total_shared_reads     = analysis.get_counter("total_shared_reads") or 0
    total_shared_reads_small   = analysis.get_counter("total_shared_reads_small") or 0
    total_shared_writes        = analysis.get_counter("total_shared_writes") or 0
    total_shared_writes_small  = analysis.get_counter("total_shared_writes_small") or 0
    slowest_rank_bytes         = analysis.get_counter("slowest_rank_bytes") or 0
    fastest_rank_bytes         = analysis.get_counter("fastest_rank_bytes") or 0
    total_transfer_size    = analysis.get_counter("total_transfer_size") or 0
    slowest_rank_time      = analysis.get_counter("slowest_rank_time") or 0 
    fastest_rank_time      = analysis.get_counter("fastest_rank_time") or 0
    total_transfer_time    = analysis.get_counter("total_transfer_time") or 0
    max_bytes_written      = analysis.get_counter("max_bytes_written") or None
    min_bytes_written      = analysis.get_counter("min_bytes_written") or None
    max_bytes_read         = analysis.get_counter("max_bytes_read") or None
    min_bytes_read         = analysis.get_counter("min_bytes_read") or None
    mpiio_coll_reads       = analysis.get_counter("mpiio_coll_reads") or 0
    mpiio_indep_reads      = analysis.get_counter("mpiio_indep_reads") or 0
    total_mpiio_read_operations = analysis.get_counter("total_mpiio_read_operations") or 0
    mpiio_coll_writes      = analysis.get_counter("mpiio_coll_writes") or 0
    mpiio_indep_writes     = analysis.get_counter("mpiio_indep_writes") or 0
    total_mpiio_write_operations = analysis.get_counter("total_mpiio_write_operations") or 0
    mpiio_nb_reads         = analysis.get_counter("mpiio_nb_reads") or 0
    mpiio_nb_writes        = analysis.get_counter("mpiio_nb_writes") or 0
    has_hdf5_extension     = analysis.get_counter("has_hdf5_extension") or False

    file_map               = analysis.get_counter("file_map") or {}
    modules                = set(analysis.get_counter("modules") or [])
    
    detected_files         = analysis.get_counter("detected_files")
    detected_files_read    = analysis.get_counter("detected_files_read")
    detected_files_write   = analysis.get_counter("detected_files_write")

    write_df_map           = analysis.get_counter("write_df_map") or {}
    write_counters         = analysis.get_counter("write_counters") or {}
    read_df_map            = analysis.get_counter("read_df_map") or {}
    read_counters         = analysis.get_counter("read_counters") or {}
    
    shared_files           = analysis.get_counter("shared_files")
    count_long_metadata    = analysis.get_counter("count_long_metadata") or 0
    stragglers_count       = analysis.get_counter("stragglers_count") or 0
    
    imbalance_count        = analysis.get_counter("imbalance_count") or 0
    imbalance_count_read   = analysis.get_counter("imbalance_count_read") or 0
    imbalance_count_write  = analysis.get_counter("imbalance_count_write") or 0

    dxt_mpiio              = analysis.get_counter("dxt_mpiio")
    dxt_posix              = analysis.get_counter("dxt_posix")
    dxt_posix_read_data    = analysis.get_counter("dxt_posix_read_data")
    dxt_posix_write_data   = analysis.get_counter("dxt_posix_write_data")
    hints                  = analysis.get_counter("hints") or []
    cb_nodes               = analysis.get_counter("cb_nodes")
    NUMBER_OF_COMPUTE_NODES = analysis.get_counter("NUMBER_OF_COMPUTE_NODES") or 0
    df_intervals = analysis.get_counter("df_intervals")
    if df_intervals is None or df_intervals.empty:
        df_intervals = pd.DataFrame(columns=["start", "end", "size", "file_id", "api", "rank"])

    df_posix = analysis.get_counter("df_posix")


    check_stdio(total_size, total_size_stdio)
    
    check_mpiio(modules)
    
    check_operation_intensive(total_operations, total_reads, total_writes)
    
    check_size_intensive(total_size, total_read_size, total_written_size)
    
    check_small_operation(total_reads, total_reads_small, total_writes, total_writes_small,
                          detected_files, modules, file_map, dxt_posix, dxt_posix_read_data, dxt_posix_write_data)
    
    check_misaligned(total_operations, total_mem_not_aligned, total_file_not_aligned,
                     modules, file_map, analysis.get_counter("df_lustre"), dxt_posix, dxt_posix_read_data)
    
    check_traffic(max_read_offset, total_read_size, max_write_offset, total_written_size,
                  dxt_posix, dxt_posix_read_data, dxt_posix_write_data)
    
    check_random_operation(read_consecutive, read_sequential, read_random, total_reads,
                           write_consecutive, write_sequential, write_random, total_writes,
                           dxt_posix, dxt_posix_read_data, dxt_posix_write_data)
    
    check_shared_small_operation(total_shared_reads, total_shared_reads_small,
                                 total_shared_writes, total_shared_writes_small,
                                 shared_files, file_map)
    
    check_long_metadata(count_long_metadata, modules)

    check_shared_data_imblance_split(slowest_rank_bytes, fastest_rank_bytes, total_transfer_size)
    
    check_shared_data_imblance(stragglers_count, detected_files, file_map,
                               dxt_posix, dxt_posix_read_data, dxt_posix_write_data)
    
    check_shared_time_imbalance_split(slowest_rank_time, fastest_rank_time, total_transfer_time)
    
    check_shared_time_imbalance(stragglers_count, detected_files, file_map)

    check_individual_write_imbalance_split(max_bytes_written, min_bytes_written)

    check_individual_read_imbalance_split(max_bytes_read, min_bytes_read)
    
    new_detected_write_list = []
    for file_id, df in write_df_map.items():
        max_bytes_written = df['size'].max()
        min_bytes_written = df['size'].min()    
        if max_bytes_written and abs(max_bytes_written - min_bytes_written) / max_bytes_written > thresholds['imbalance_size'][0]:
            imbalance_count_write += 1
            imbalance_percentage = abs(max_bytes_written - min_bytes_written) / max_bytes_written * 100
            new_detected_write_list.append([file_id, imbalance_percentage])
    column_names = ['id', 'write_imbalance']
    new_detected_df = pd.DataFrame(new_detected_write_list, columns=column_names)
    # If detected_files already exists and is not empty, concatenate the new data with it.
    if detected_files is not None and not detected_files.empty:
        # Concatenate along the rows and reset the index.
        detected_files = pd.concat([detected_files, new_detected_df], ignore_index=True)
    else:
        detected_files = new_detected_df
    check_individual_write_imbalance(imbalance_count_write, detected_files, file_map, dxt_posix, dxt_posix_write_data)
      
    
    new_detected_read_list = []
    for file_id, df in read_df_map.items():  
        max_bytes_read = df['size'].max()
        min_bytes_read = df['size'].min()
        if max_bytes_read and abs(max_bytes_read - min_bytes_read) / max_bytes_read > thresholds['imbalance_size'][0]:
            imbalance_count_read += 1
            imbalance_percentage_read = abs(max_bytes_read - min_bytes_read) / max_bytes_read * 100
            new_detected_read_list.append([file_id, imbalance_percentage_read])
    column_names = ['id', 'read_imbalance']
    new_detected_read_df = pd.DataFrame(new_detected_read_list, columns=column_names)
    if detected_files is not None and not detected_files.empty:
        detected_files = pd.concat([detected_files, new_detected_read_df], ignore_index=True)
    else:
        detected_files = new_detected_read_df
    check_individual_read_imbalance(imbalance_count_read, detected_files, file_map, dxt_posix, dxt_posix_read_data)
    
    
    check_mpi_collective_read_operation(mpiio_coll_reads, mpiio_indep_reads, total_mpiio_read_operations,
                                         detected_files, file_map, dxt_mpiio)
    
    check_mpi_collective_write_operation(mpiio_coll_writes, mpiio_indep_writes, total_mpiio_write_operations,
                                          detected_files, file_map, dxt_mpiio)
    
    check_mpi_none_block_operation(mpiio_nb_reads, mpiio_nb_writes, has_hdf5_extension, modules)
    
    if 'MPI-IO' in modules:
        try:
            cb_nodes = int(cb_nodes)
        except (ValueError, TypeError):
            cb_nodes = 0
        check_mpi_aggregator(cb_nodes, NUMBER_OF_COMPUTE_NODES)


    # Display final Drishti panel.
    job          = analysis.get_counter("job") or {}
    job_start    = analysis.get_counter("job_start") or datetime.datetime.now()
    job_end      = analysis.get_counter("job_end") or datetime.datetime.now()
    total_files  = analysis.get_counter("total_files") or 0
    total_files_stdio = analysis.get_counter("total_files_stdio") or 0
    total_files_posix = analysis.get_counter("total_files_posix") or 0
    total_files_mpiio = analysis.get_counter("total_files_mpiio") or 0
    
    if trace_type == "darshan":
        display_drishti_output_darshan(
            job,
            job_start,
            job_end,
            total_files,
            total_files_stdio,
            total_files_posix,
            total_files_mpiio,
            NUMBER_OF_COMPUTE_NODES,
            hints
        )
    elif trace_type == "recorder":
        display_drishti_output_recorder(
            total_files,
            total_files_stdio,
            total_files_posix,
            total_files_mpiio,
            df_intervals
        )
    #console.print()
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
    print("MPI-IO Collective Reads:", analysis.get_counter("mpiio_coll_reads"))
    print("MPI-IO Independent Reads:", analysis.get_counter("mpiio_indep_reads"))
    print("Total MPI-IO Read Ops:", analysis.get_counter("total_mpiio_read_operations"))
    print("MPI-IO Collective Writes:", analysis.get_counter("mpiio_coll_writes"))
    print("MPI-IO Independent Writes:", analysis.get_counter("mpiio_indep_writes"))
    print("Total MPI-IO Write Ops:", analysis.get_counter("total_mpiio_write_operations"))
    print("MPI-IO Non-blocking Reads:", analysis.get_counter("mpiio_nb_reads"))
    print("MPI-IO Non-blocking Writes:", analysis.get_counter("mpiio_nb_writes"))

    print("max_bytes_written:", analysis.get_counter("max_bytes_written"))
    print("min_bytes_written:", analysis.get_counter("min_bytes_written"))
    print("imbalance count write:", analysis.get_counter("imbalance_count_write"))
    print("imbalance count read:", analysis.get_counter("imbalance_count_read"))
    print("detected_files:", analysis.get_counter("detected_files"))

    print(df_intervals.head())

    """
    #extra information 
    print("Has HDF5 Extension:", analysis.get_counter("has_hdf5_extension"))
    print("File Map:", analysis.get_counter("file_map"))
    print("Modules:", analysis.get_counter("modules"))
    print("Detected Files:", analysis.get_counter("detected_files"))
    print("Shared Files:", analysis.get_counter("shared_files"))
    print("Count Long Metadata:", analysis.get_counter("count_long_metadata"))
    print("Stragglers Count:", analysis.get_counter("stragglers_count"))
    print("Imbalance Count:", analysis.get_counter("imbalance_count"))
    print("DXT MPIIO:", analysis.get_counter("dxt_mpiio"))
    print("DXT POSIX:", analysis.get_counter("dxt_posix"))
    print("DXT POSIX Read Data:", analysis.get_counter("dxt_posix_read_data"))
    print("DXT POSIX Write Data:", analysis.get_counter("dxt_posix_write_data"))
    print("Hints:", analysis.get_counter("hints"))
    print("CB Nodes:", analysis.get_counter("cb_nodes"))
    print("Number of Compute Nodes:", analysis.get_counter("NUMBER_OF_COMPUTE_NODES"))


    """
    


if __name__ == "__main__":
    main()
