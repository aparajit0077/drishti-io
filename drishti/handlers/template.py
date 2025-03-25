
class HPCAnalysisBlackBox():
    def __init__(self):
        # Internal dictionary for counters
        self._counters = {}
        # register MPI-IO counters
        drishti_counters = [
            "total_write_size_stdio",
            "total_read_size_stdio",
            "total_size_stdio",
            "total_write_size_posix",
            "total_read_size_posix",
            "total_size_posix",
            "total_write_size_mpiio",
            "total_read_size_mpiio",
            "total_size_mpiio",
            "total_size",
            "total_reads",
            "total_writes",
            "total_operations",
            "total_read_size",
            "total_written_size",
            "total_reads_small",
            "total_writes_small",
            "total_mem_not_aligned",
            "total_file_not_aligned",
            "max_read_offset",
            "max_write_offset",
            "read_consecutive",
            "read_sequential",
            "read_random",
            "write_consecutive",
            "write_sequential",
            "write_random",
            "total_shared_reads",
            "total_shared_reads_small",
            "total_shared_writes",
            "total_shared_writes_small",
            "slowest_rank_bytes", 
            "fastest_rank_bytes",
            "total_transfer_size",
            "slowest_rank_time", 
            "fastest_rank_time",
            "total_transfer_time",
            "max_bytes_written", 
            "min_bytes_written",
            "max_bytes_read", 
            "min_bytes_read",
            "mpiio_coll_reads",
            "mpiio_indep_reads",
            "total_mpiio_read_operations",
            "mpiio_coll_writes",
            "mpiio_indep_writes",
            "total_mpiio_write_operations",
            "mpiio_nb_reads",
            "mpiio_nb_writes",
            "df_lustre",
            "dxt_posix",
            "dxt_posix_read_data",
            "dxt_posix_write_data",
            "modules",
            "file_map",
            "detected_files",
            "shared_files",
            "count_long_metadata",
            "stragglers_count",
            "imbalance_count",
            "dxt_mpiio",
            "has_hdf5_extension",
            "hints",
            "cb_nodes",
            "NUMBER_OF_COMPUTE_NODES",
            "job",
            "job_start",
            "job_end",
            "total_files",
            "total_files_stdio",
            "total_files_posix",
            "total_files_mpiio",
            "df_intervals",
        ]
        for name in drishti_counters:
            self._register_counter(name)
        
    def _register_counter(self, name: str) -> None:
        """
        [Internal Use Only]
        Register a new counter, initializing it to None.
        """
        self._counters[name] = None

    def set_counter(self, name: str, value) -> None:
        """
        Store 'value' for a previously registered counter.
        """
        if name not in self._counters:
            raise KeyError(f"Counter '{name}' is not registered.")
        self._counters[name] = value

    def get_counter(self, name: str):
        """
        Retrieve the current value of a registered counter.
        """
        if name not in self._counters:
            raise KeyError(f"Counter '{name}' is not defined.")
        return self._counters[name]

class DrishtiAnalysis(HPCAnalysisBlackBox):
    def load_data(self):
        pass




