import subprocess
from pathlib import Path
from typing import Tuple

from latch import large_task, message, small_task, workflow
from latch.resources.tasks import cached_large_task
from latch.types import LatchDir, LatchFile

from .types import HostData, Sample

CACHE_VERSION = "0.1.0"


@small_task
def fastp(
    sample: Sample,
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
        sample.read1.local_path,
        "--in2",
        sample.read2.local_path,
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
    message(
        "info",
        {
            "title": "Running fastp to remove low-quality reads",
            "body": f"Command: {' '.join(_fastp_cmd)}",
        },
    )
    subprocess.run(_fastp_cmd)

    return LatchDir(
        str(output_dir), f"latch:///metamage/{sample_name}/{output_dir_name}"
    )


# @cached_large_task(CACHE_VERSION)
@large_task
def build_bowtie_index(
    host_data: HostData,
    sample_name: str,
) -> LatchDir:

    output_dir_name = f"{sample_name}_btidx"
    output_dir = Path(output_dir_name).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    host_name_clean = host_data.host_name.replace(" ", "_").lower()

    _bt_idx_cmd = [
        "bowtie2/bowtie2-build",
        host_data.host_genome.local_path,
        f"{str(output_dir)}/{host_name_clean}",
        "--threads",
        "31",
    ]
    message(
        "info",
        {
            "title": "Building bowtie2 index for the host genome",
            "body": f"Command: {' '.join(_bt_idx_cmd)}",
        },
    )
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
    host_data: HostData,
) -> LatchDir:

    output_dir_name = f"{sample_name}_bt_unaligned"
    output_dir = Path(output_dir_name).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    host_name_clean = host_data.host_name.replace(" ", "_").lower()

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
    message(
        "info",
        {
            "title": "Aligning to host genome",
            "body": f"Command: {' '.join(_bt_cmd)}",
        },
    )
    subprocess.run(_bt_cmd)

    return LatchDir(
        str(output_dir), f"latch:///metamage/{sample_name}/{output_dir_name}"
    )


@workflow
def host_removal_wf(
    sample: Sample,
    host_data: HostData,
    sample_name: str,
) -> LatchDir:

    # Preprocessing
    trimmed_data = fastp(sample=sample, sample_name=sample_name)

    # Host read removal
    host_idx = build_bowtie_index(sample_name=sample_name, host_data=host_data)

    unaligned = map_to_host(
        host_idx=host_idx,
        read_dir=trimmed_data,
        sample_name=sample_name,
        host_data=host_data,
    )

    return unaligned
