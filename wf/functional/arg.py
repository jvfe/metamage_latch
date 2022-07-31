import subprocess
from pathlib import Path

from latch import small_task
from latch.types import LatchDir

from ..types import fARGeneModel


@small_task
def fargene(
    assembly_dir: LatchDir, sample_name: str, hmm_model: fARGeneModel
) -> LatchDir:

    # Assembly data
    assembly_name = f"{sample_name}.contigs.fa"
    assembly_fasta = Path(assembly_dir.local_path, assembly_name)

    output_dir_name = "fargene_results"
    outdir = Path(output_dir_name).resolve()

    _fargene_cmd = [
        "fargene",
        "-i",
        str(assembly_fasta),
        "--hmm-model",
        hmm_model.value,
        "-o",
        output_dir_name,
        "-p",
        "8",
    ]

    subprocess.run(_fargene_cmd)

    return LatchDir(str(outdir), f"latch:///maggie/{sample_name}/{output_dir_name}")
