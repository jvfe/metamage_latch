from typing import List, Union

from latch import workflow
from latch.resources.launch_plan import LaunchPlan
from latch.types import LatchDir, LatchFile

from .docs import MAGGIE_DOCS
from .functional.amp import macrel
from .functional.arg import fargene
from .functional.bgc import gecco
from .functional.prodigal import prodigal
from .kaiju import (
    kaiju2krona_task,
    kaiju2table_task,
    plot_krona_task,
    taxonomy_classification_task,
)
from .metassembly import megahit, metabat2, metaquast
from .types import ProdigalOutput, TaxonRank, fARGeneModel


@workflow(MAGGIE_DOCS)
def maggie(
    read1: LatchFile,
    read2: LatchFile,
    kaiju_ref_db: LatchFile,
    kaiju_ref_nodes: LatchFile,
    kaiju_ref_names: LatchFile,
    sample_name: str = "maggie_sample",
    taxon_rank: TaxonRank = TaxonRank.species,
    min_count: str = "2",
    k_min: str = "21",
    k_max: str = "141",
    k_step: str = "12",
    min_contig_len: str = "200",
    prodigal_output_format: ProdigalOutput = ProdigalOutput.gbk,
    fargene_hmm_model: fARGeneModel = fARGeneModel.class_a,
) -> List[Union[LatchFile, LatchDir]]:
    """Metagenomic pre-processing, assembly, annotation and binning

    maggie
    ----------

    maggie is a workflow for taxonomic classification, assembly, binning
    and annotation of long-read metagenomics datasets. It's composed of:

    - fastp for read trimming and other general pre-processing
    - BowTie2 for mapping to the host genome and extracting unaligned reads

    - [MEGAHIT](https://github.com/voutcn/megahit) for assembly
    - [MetaQuast](https://github.com/ablab/quast) for assembly evaluation
    - [Macrel](https://github.com/BigDataBiology/macrel) for predicting Antimicrobial Peptide
      (AMP)-like sequences from assembly_dir
    - [fARGene](https://github.com/fannyhb/fargene) for identifying Antimicrobial Resistance Genes
      (ARGs) from assembly_dir
    - [Gecco](https://github.com/zellerlab/GECCO) for predicting biosynthetic gene clusters
      (BCGs) from assembly_dir
    - [Prodigal](https://github.com/hyattpd/Prodigal) for protein-coding
      gene prediction from assembly_dir.

    - [MetaBAT2](https://bitbucket.org/berkeleylab/metabat/src/master/) for
      binning

    - [Kaiju](https://github.com/bioinformatics-centre/kaiju) for
      taxonomic classification
    - [KronaTools](https://github.com/marbl/Krona/wiki/KronaTools) for
      visualizing taxonomic classification results

    ---

    ### References

    Li, D., Luo, R., Liu, C.M., Leung, C.M., Ting, H.F., Sadakane, K., Yamashita, H. and Lam, T.W., 2016. MEGAHIT v1.0: A Fast and Scalable Metagenome Assembler driven by Advanced Methodologies and Community Practices. Methods.

    Alla Mikheenko, Vladislav Saveliev, Alexey Gurevich,
    MetaQUAST: evaluation of metagenome assemblies,
    Bioinformatics (2016) 32 (7): 1088-1090. doi: 10.1093/bioinformatics/btv697

    Kang DD, Li F, Kirton E, Thomas A, Egan R, An H, Wang Z. 2019. MetaBAT 2: an
    adaptive binning algorithm for robust and efficient genome reconstruction
    from metagenome assemblies. PeerJ 7:e7359 https://doi.org/10.7717/peerj.7359

    Menzel, P., Ng, K. & Krogh, A. Fast and sensitive taxonomic classification for
    metagenomics with Kaiju. Nat Commun 7, 11257 (2016).
    https://doi.org/10.1038/ncomms11257

    Hyatt, D., Chen, GL., LoCascio, P.F. et al. Prodigal: prokaryotic gene recognition
    and translation initiation site identification.
    BMC Bioinformatics 11, 119 (2010). https://doi.org/10.1186/1471-2105-11-119

    Santos-Júnior CD, Pan S, Zhao X, Coelho LP. 2020.
    Macrel: antimicrobial peptide screening in genomes and metagenomes.
    PeerJ 8:e10555. DOI: 10.7717/peerj.10555

    Berglund, F., Österlund, T., Boulund, F., Marathe, N. P.,
    Larsson, D. J., & Kristiansson, E. (2019).
    Identification and reconstruction of novel antibiotic resistance genes
    from metagenomes. Microbiome, 7(1), 52.

    Accurate de novo identification of biosynthetic gene clusters with GECCO.
    Laura M Carroll, Martin Larralde, Jonas Simon Fleck, Ruby Ponnudurai,
    Alessio Milanese, Elisa Cappio Barazzone, Georg Zeller.
    bioRxiv 2021.05.03.442509; doi:10.1101/2021.05.03.442509
    """
    kaiju_out = taxonomy_classification_task(
        read1=read1,
        read2=read2,
        kaiju_ref_db=kaiju_ref_db,
        kaiju_ref_nodes=kaiju_ref_nodes,
        sample=sample_name,
    )
    kaiju2table_out = kaiju2table_task(
        kaiju_out=kaiju_out,
        sample=sample_name,
        kaiju_ref_nodes=kaiju_ref_nodes,
        kaiju_ref_names=kaiju_ref_names,
        taxon=taxon_rank,
    )
    kaiju2krona_out = kaiju2krona_task(
        kaiju_out=kaiju_out,
        sample=sample_name,
        kaiju_ref_nodes=kaiju_ref_nodes,
        kaiju_ref_names=kaiju_ref_names,
    )
    krona_plot = plot_krona_task(krona_txt=kaiju2krona_out, sample=sample_name)

    assembly_dir = megahit(
        read_1=read1,
        read_2=read2,
        sample_name=sample_name,
        min_count=min_count,
        k_min=k_min,
        k_max=k_max,
        k_step=k_step,
        min_contig_len=min_contig_len,
    )
    metassembly_results = metaquast(assembly_dir=assembly_dir, sample_name=sample_name)
    binning_results = metabat2(assembly_dir=assembly_dir, sample_name=sample_name)

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

    return [
        kaiju2table_out,
        krona_plot,
        metassembly_results,
        binning_results,
        prodigal_results,
        macrel_results,
        fargene_results,
        gecco_results,
    ]


LaunchPlan(
    maggie,  # workflow name
    "Example Metagenome (Crohn's disease gut microbiome)",  # name of test data
    {
        "read1": LatchFile("latch:///Crohn/SRR579292_1.fastq"),
        "read2": LatchFile("latch:///Crohn/SRR579292_2.fastq"),
        "kaiju_ref_db": LatchFile("latch:///kaiju_idx/kaiju_db_viruses.fmi"),
        "kaiju_ref_nodes": LatchFile("latch:///kaiju_idx/nodes.dmp"),
        "kaiju_ref_names": LatchFile("latch:///kaiju_idx/names.dmp"),
        "sample_name": "crohn_data1",
        "taxon_rank": TaxonRank.species,
        "min_count": "2",
        "k_min": "21",
        "k_max": "141",
        "k_step": "12",
        "min_contig_len": "200",
        "prodigal_output_format": ProdigalOutput.gff,
        "fargene_hmm_model": fARGeneModel.class_b_1_2,
    },
)
