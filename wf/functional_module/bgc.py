import subprocess
from pathlib import Path

from latch import message, small_task
from latch.types import LatchDir


@small_task
def gecco(assembly_dir: LatchDir, sample_name: str) -> LatchDir:

    # Assembly data
    assembly_name = f"{sample_name}.contigs.fa"
    assembly_fasta = Path(assembly_dir.local_path, assembly_name)

    output_dir_name = "gecco_results"
    outdir = Path(output_dir_name).resolve()

    _gecco_cmd = [
        "gecco",
        "run",
        "-g",
        str(assembly_fasta),
        "-o",
        output_dir_name,
        "-j",
        "4",
        "--force-tsv",
    ]
    message(
        "info",
        {
            "title": "Detecting bacterial gene clusters in contigs with Gecco",
            "body": f"Command: {' '.join(_gecco_cmd)}",
        },
    )
    subprocess.run(_gecco_cmd)

    return LatchDir(str(outdir), f"latch:///metamage/{sample_name}/{output_dir_name}")
