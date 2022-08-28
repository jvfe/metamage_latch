import subprocess
from pathlib import Path
from typing import Tuple

from latch import large_task, small_task, workflow
from latch.resources.tasks import cached_large_task
from latch.types import LatchDir, LatchFile

CACHE_VERSION = "0.1.0"


@small_task
def fastp(
    read1: LatchFile,
    read2: LatchFile,
    sample_name: str,
) -> LatchDir:
    """Adapter removal and read trimming with fastp"""

    output_dir_name = "fastp_results"
    output_dir = Path(output_dir_name).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    output_prefix = f"{str(output_dir)}/{sample_name}"

    _fastp_cmd = [
        "/root/fastp",
        "--in1",
        read1.local_path,
        "--in2",
        read2.local_path,
        "--out1",
        f"{output_prefix}_1.trim.fastq.gz",
        "--out2",
        f"{output_prefix}_2.trim.fastq.gz",
        "--json",
        f"{output_prefix}.fastp.json",
        "--html",
        f"{output_prefix}.fastp.html",
        "--thread",
        "4",
        "--detect_adapter_for_pe",
    ]

    subprocess.run(_fastp_cmd)

    return LatchDir(
        str(output_dir), f"latch:///metamage/{sample_name}/{output_dir_name}"
    )


# @cached_large_task(CACHE_VERSION)
@large_task
def build_bowtie_index(
    host_genome: LatchFile, sample_name: str, host_name: str
) -> LatchDir:

    output_dir_name = f"{sample_name}_btidx"
    output_dir = Path(output_dir_name).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    host_name_clean = host_name.replace(" ", "_").lower()

    _bt_idx_cmd = [
        "bowtie2/bowtie2-build",
        host_genome.local_path,
        f"{str(output_dir)}/{host_name_clean}",
        "--threads",
        "31",
    ]

    subprocess.run(_bt_idx_cmd)

    return LatchDir(
        str(output_dir), f"latch:///metamage/{sample_name}/{output_dir_name}"
    )


# @cached_large_task(CACHE_VERSION)
@large_task
def map_to_host(
    host_idx: LatchDir,
    read_dir: LatchDir,
    sample_name: str,
    host_name: str,
) -> LatchDir:

    output_dir_name = f"{sample_name}_bt_unaligned"
    output_dir = Path(output_dir_name).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    host_name_clean = host_name.replace(" ", "_").lower()

    _bt_cmd = [
        "bowtie2/bowtie2",
        "-x",
        f"{host_idx.local_path}/{host_name_clean}",
        "-1",
        f"{read_dir.local_path}/{sample_name}_1.trim.fastq.gz",
        "-2",
        f"{read_dir.local_path}/{sample_name}_2.trim.fastq.gz",
        "--un-conc-gz",
        f"{output_dir}/{sample_name}_unaligned.fastq.gz",
        "--threads",
        "31",
    ]

    subprocess.run(_bt_cmd)

    return LatchDir(
        str(output_dir), f"latch:///metamage/{sample_name}/{output_dir_name}"
    )


@workflow
def host_removal_wf(
    read1: LatchFile,
    read2: LatchFile,
    host_genome: LatchFile,
    host_name: str,
    sample_name: str,
) -> LatchDir:

    # Preprocessing
    trimmed_data = fastp(read1=read1, read2=read2, sample_name=sample_name)

    # Host read removal
    host_idx = build_bowtie_index(
        host_genome=host_genome, sample_name=sample_name, host_name=host_name
    )

    unaligned = map_to_host(
        host_idx=host_idx,
        read_dir=trimmed_data,
        sample_name=sample_name,
        host_name=host_name,
    )

    return unaligned
