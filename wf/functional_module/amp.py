import subprocess
from pathlib import Path

from latch import small_task
from latch.types import LatchDir


@small_task
def macrel(assembly_dir: LatchDir, sample_name: str) -> LatchDir:

    # Assembly data
    assembly_name = f"{sample_name}.contigs.fa"
    assembly_fasta = Path(assembly_dir.local_path, assembly_name)

    output_dir_name = "macrel_results"
    outdir = Path(output_dir_name).resolve()

    _macrel_cmd = [
        "macrel",
        "contigs",
        "--fasta",
        str(assembly_fasta),
        "--output",
        str(outdir),
        "--tag",
        sample_name,
        "--log-file",
        f"{str(outdir)}/{sample_name}_log.txt",
        "--threads",
        "8",
    ]

    subprocess.run(_macrel_cmd)

    return LatchDir(str(outdir), f"latch:///metamage/{sample_name}/{output_dir_name}")
