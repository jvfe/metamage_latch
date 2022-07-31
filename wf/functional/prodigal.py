"""
Predict protein-coding genes with prodigal
"""

import subprocess
from pathlib import Path

from latch import large_task
from latch.types import LatchDir

from ..types import ProdigalOutput


@large_task
def prodigal(
    assembly_dir: LatchDir, sample_name: str, output_format: ProdigalOutput
) -> LatchDir:

    # Assembly data
    assembly_name = f"{sample_name}.contigs.fa"
    assembly_fasta = Path(assembly_dir.local_path, assembly_name)

    # A reference to our output.
    output_dir_name = "prodigal_results"
    output_dir = Path(output_dir_name).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir.joinpath(f"{sample_name}.{output_format.value}")
    output_proteins = output_dir.joinpath(f"{sample_name}.faa")
    output_genes = output_dir.joinpath(f"{sample_name}.fna")
    output_scores = output_dir.joinpath(f"{sample_name}.cds")

    _prodigal_cmd = [
        "/root/prodigal",
        "-i",
        str(assembly_fasta),
        "-f",
        output_format.value,
        "-o",
        str(output_file),
        "-a",
        str(output_proteins),
        "-d",
        str(output_genes),
        "-s",
        str(output_scores),
    ]

    subprocess.run(_prodigal_cmd)

    return LatchDir(str(output_dir), f"latch:///maggie/{sample_name}/{output_dir_name}")
