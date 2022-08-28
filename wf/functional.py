from typing import Tuple

from latch import workflow
from latch.types import LatchDir

from .functional_module.amp import macrel
from .functional_module.arg import fargene
from .functional_module.bgc import gecco
from .functional_module.prodigal import prodigal
from .types import ProdigalOutput, fARGeneModel


@workflow
def functional_wf(
    assembly_dir: LatchDir,
    sample_name: str,
    prodigal_output_format: ProdigalOutput,
    fargene_hmm_model: fARGeneModel,
) -> Tuple[LatchDir, LatchDir, LatchDir, LatchDir]:

    # Functional annotation
    prodigal_results = prodigal(
        assembly_dir=assembly_dir,
        sample_name=sample_name,
        output_format=prodigal_output_format,
    )
    macrel_results = macrel(assembly_dir=assembly_dir, sample_name=sample_name)
    fargene_results = fargene(
        assembly_dir=assembly_dir, sample_name=sample_name, hmm_model=fargene_hmm_model
    )
    gecco_results = gecco(assembly_dir=assembly_dir, sample_name=sample_name)

    return prodigal_results, macrel_results, fargene_results, gecco_results
