"""
Read assembly and evaluation for metagenomics data
"""

import subprocess
from pathlib import Path

from latch import large_task, small_task
from latch.types import LatchDir, LatchFile


@large_task
def megahit(
    read_1: LatchFile,
    read_2: LatchFile,
    sample_name: str,
    min_count: str,
    k_min: str,
    k_max: str,
    k_step: str,
    min_contig_len: str,
) -> LatchDir:
    output_dir_name = "MEGAHIT"
    output_dir = Path(output_dir_name).resolve()
    _megahit_cmd = [
        "/root/megahit",
        "--min-count",
        min_count,
        "--k-min",
        k_min,
        "--k-max",
        k_max,
        "--k-step",
        k_step,
        "--out-dir",
        output_dir_name,
        "--out-prefix",
        sample_name,
        "--min-contig-len",
        min_contig_len,
        "-1",
        read_1.local_path,
        "-2",
        read_2.local_path,
    ]

    subprocess.run(_megahit_cmd)

    return LatchDir(
        str(output_dir), f"latch:///maggie/{sample_name}/{output_dir_name}"
    )


@small_task
def metaquast(
    assembly_dir: LatchDir,
    sample_name: str,
) -> LatchDir:

    assembly_name = f"{sample_name}.contigs.fa"
    assembly_fasta = Path(assembly_dir.local_path, assembly_name)

    output_dir_name = "MetaQuast"
    output_dir = Path(output_dir_name).resolve()

    _metaquast_cmd = [
        "/root/metaquast.py",
        "--rna-finding",
        "--no-sv",
        "--max-ref-number",
        "0",
        "-l",
        sample_name,
        "-o",
        output_dir_name,
        str(assembly_fasta),
    ]

    subprocess.run(_metaquast_cmd)

    return LatchDir(
        str(output_dir), f"latch:///maggie/{sample_name}/{output_dir_name}"
    )


@large_task
def metabat2(
    assembly_dir: LatchDir,
    sample_name: str,
) -> LatchDir:

    assembly_name = f"{sample_name}.contigs.fa"
    assembly_fasta = Path(assembly_dir.local_path, assembly_name)

    output_dir_name = f"METABAT/{sample_name}"
    output_dir = Path(output_dir_name).parent.resolve()

    _metabat_cmd = [
        "metabat2",
        "--saveCls",
        "-i",
        str(assembly_fasta),
        "-o",
        output_dir_name,
    ]

    subprocess.run(_metabat_cmd)

    return LatchDir(str(output_dir), f"latch:///maggie/{sample_name}/METABAT/")
