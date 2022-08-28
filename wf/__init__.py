from typing import List, Union

from latch import workflow
from latch.resources.launch_plan import LaunchPlan
from latch.types import LatchDir, LatchFile

from .binning import (
    bowtie_assembly_align,
    bowtie_assembly_build,
    metabat2,
    summarize_contig_depths,
)
from .docs import metamage_DOCS
from .functional.amp import macrel
from .functional.arg import fargene
from .functional.bgc import gecco
from .functional.prodigal import prodigal
from .host_removal import build_bowtie_index, fastp, map_to_host
from .kaiju import kaiju_wf
from .metassembly import megahit, metaquast
from .types import ProdigalOutput, TaxonRank, fARGeneModel


@workflow(metamage_DOCS)
def metamage(
    read1: LatchFile,
    read2: LatchFile,
    host_genome: LatchFile,
    kaiju_ref_db: LatchFile,
    kaiju_ref_nodes: LatchFile,
    kaiju_ref_names: LatchFile,
    host_name: str = "host",
    sample_name: str = "metamage_sample",
    taxon_rank: TaxonRank = TaxonRank.species,
    min_count: int = 2,
    k_min: int = 21,
    k_max: int = 141,
    k_step: int = 12,
    min_contig_len: int = 200,
    prodigal_output_format: ProdigalOutput = ProdigalOutput.gbk,
    fargene_hmm_model: fARGeneModel = fARGeneModel.class_a,
) -> List[Union[LatchFile, LatchDir]]:
    """Metagenomic pre-processing, assembly, annotation and binning

    metamage
    ----------

    metamage is a workflow for taxonomic classification, assembly, binning
    and annotation of short-read host-associated metagenomics datasets.

    ![MetaMage Graph](https://i.imgur.com/Fo464EY.png)

    It's composed of:

    ## Read pre-processing and host read removal

    - [fastp](https://github.com/OpenGene/fastp) for read trimming
      and other general pre-processing [^9]
    - [BowTie2](https://github.com/BenLangmead/bowtie2) for mapping
      to the host genome and extracting unaligned reads [^10]

    ## Assembly

    - [MEGAHIT](https://github.com/voutcn/megahit) for assembly [^1]
    - [MetaQuast](https://github.com/ablab/quast) for assembly evaluation

    ## Functional annotation

    - [Macrel](https://github.com/BigDataBiology/macrel) for predicting Antimicrobial Peptide
      (AMP)-like sequences from contigs [^6]
    - [fARGene](https://github.com/fannyhb/fargene) for identifying Antimicrobial Resistance Genes
      (ARGs) from contigs [^7]
    - [Gecco](https://github.com/zellerlab/GECCO) for predicting biosynthetic gene clusters
      (BCGs) from contigs [^8]
    - [Prodigal](https://github.com/hyattpd/Prodigal) for protein-coding
      gene prediction from contigs. [^5]

    ## Binning

    - BowTie2 and [Samtools](https://github.com/samtools/samtools)[^11] to
      building depth files for binning.
    - [MetaBAT2](https://bitbucket.org/berkeleylab/metabat/src/master/) for
      binning [^2]

    ## Taxonomic classification of reads

    - [Kaiju](https://github.com/bioinformatics-centre/kaiju) for
      taxonomic classification [^3]
    - [KronaTools](https://github.com/marbl/Krona/wiki/KronaTools) for
      visualizing taxonomic classification results

    # Output tree

    - |metamage
      - |{sample_name}
        - |{sample_name}_bt_idx - Host genome BowTie index
        - |{sample_name}_bt_unaligned - Reads that didn't align to the host genome
        - |fastp_results - Results from trimming with fastp
        - |kaiju
        - |MEGAHIT
        - |MetaQuast - Assembly evaluation report
        - |{sample_name}_assembly_idx - BowTie Index from assembly data
        - |{sample_name}_assembly_sorted.bam - Reads aligned to assembly contigs
        - |METABAT
        - |fargene_results
        - |gecco_results
        - |macrel_results
        - |prodigal_results

    # Where to get the data?

    - Kaiju indexes can be generated based on a reference database but
      you can also find some pre-built ones in the sidebar of the
      [Kaiju website](https://kaiju.binf.ku.dk/server).

    - Reference host genomes can be acquired from a variety of databases,
      for example [Ensembl](https://www.ensembl.org/index.html).

    ---

    [^1]: Li, D., Luo, R., Liu, C.M., Leung, C.M., Ting, H.F., Sadakane, K., Yamashita, H. and Lam, T.W., 2016. MEGAHIT v1.0: A Fast and Scalable Metagenome Assembler driven by Advanced Methodologies and Community Practices. Methods.

    [^2]: Alla Mikheenko, Vladislav Saveliev, Alexey Gurevich,
    MetaQUAST: evaluation of metagenome assemblies,
    Bioinformatics (2016) 32 (7): 1088-1090. doi: 10.1093/bioinformatics/btv697

    [^3]: Kang DD, Li F, Kirton E, Thomas A, Egan R, An H, Wang Z. 2019. MetaBAT 2: an
    adaptive binning algorithm for robust and efficient genome reconstruction
    from metagenome assemblies. PeerJ 7:e7359 https://doi.org/10.7717/peerj.7359

    [^4]: Menzel, P., Ng, K. & Krogh, A. Fast and sensitive taxonomic classification for
    metagenomics with Kaiju. Nat Commun 7, 11257 (2016).
    https://doi.org/10.1038/ncomms11257

    [^5]: Hyatt, D., Chen, GL., LoCascio, P.F. et al. Prodigal: prokaryotic gene recognition
    and translation initiation site identification.
    BMC Bioinformatics 11, 119 (2010). https://doi.org/10.1186/1471-2105-11-119

    [^6]: Santos-Júnior CD, Pan S, Zhao X, Coelho LP. 2020.
    Macrel: antimicrobial peptide screening in genomes and metagenomes.
    PeerJ 8:e10555. DOI: 10.7717/peerj.10555

    [^7]: Berglund, F., Österlund, T., Boulund, F., Marathe, N. P.,
    Larsson, D. J., & Kristiansson, E. (2019).
    Identification and reconstruction of novel antibiotic resistance genes
    from metagenomes. Microbiome, 7(1), 52.

    [^8]: Accurate de novo identification of biosynthetic gene clusters with GECCO.
    Laura M Carroll, Martin Larralde, Jonas Simon Fleck, Ruby Ponnudurai,
    Alessio Milanese, Elisa Cappio Barazzone, Georg Zeller.
    bioRxiv 2021.05.03.442509; doi:10.1101/2021.05.03.442509

    [^9]: Shifu Chen, Yanqing Zhou, Yaru Chen, Jia Gu;
    fastp: an ultra-fast all-in-one FASTQ preprocessor,
    Bioinformatics, Volume 34, Issue 17, 1 September 2018,
    Pages i884–i890, https://doi.org/10.1093/bioinformatics/bty560

    [^10]: Langmead B, Wilks C., Antonescu V., Charles R. Scaling read
    aligners to hundreds of threads on general-purpose processors.
    Bioinformatics. bty648.

    [^11]: Twelve years of SAMtools and BCFtools
    Petr Danecek, James K Bonfield, Jennifer Liddle, John Marshall,
    Valeriu Ohan, Martin O Pollard, Andrew Whitwham, Thomas Keane, Shane A McCarthy,
    Robert M Davies, Heng Li
    GigaScience, Volume 10, Issue 2, February 2021, giab008,
    https://doi.org/10.1093/gigascience/giab008
    """
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

    # Kaiju taxonomic classification
    kaiju2table, krona_plot = kaiju_wf(
        read_dir=unaligned,
        kaiju_ref_db=kaiju_ref_db,
        kaiju_ref_nodes=kaiju_ref_nodes,
        kaiju_ref_names=kaiju_ref_names,
        sample_name=sample_name,
        taxon_rank=taxon_rank,
    )

    # Assembly
    assembly_dir = megahit(
        read_dir=unaligned,
        sample_name=sample_name,
        min_count=min_count,
        k_min=k_min,
        k_max=k_max,
        k_step=k_step,
        min_contig_len=min_contig_len,
    )
    metassembly_results = metaquast(assembly_dir=assembly_dir, sample_name=sample_name)

    # Binning preparation
    built_assembly_idx = bowtie_assembly_build(
        assembly_dir=assembly_dir, sample_name=sample_name
    )
    aligned_to_assembly = bowtie_assembly_align(
        assembly_idx=built_assembly_idx, read_dir=unaligned, sample_name=sample_name
    )
    depth_file = summarize_contig_depths(
        assembly_bam=aligned_to_assembly, sample_name=sample_name
    )

    # Binning
    binning_results = metabat2(
        assembly_dir=assembly_dir, depth_file=depth_file, sample_name=sample_name
    )

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

    return [
        kaiju2table,
        krona_plot,
        metassembly_results,
        binning_results,
        prodigal_results,
        macrel_results,
        fargene_results,
        gecco_results,
    ]


LaunchPlan(
    metamage,  # workflow name
    "Example Metagenome (Crohn's disease gut microbiome)",  # name of test data
    {
        "read1": LatchFile("s3://latch-public/test-data/4318/SRR579292_1.fastq"),
        "read2": LatchFile("s3://latch-public/test-data/4318/SRR579292_2.fastq"),
        "host_genome": LatchFile(
            "s3://latch-public/test-data/4318/Homo_sapiens.GRCh38.dna_rm.toplevel.fa.gz"
        ),
        "host_name": "homo_sapiens",
        "kaiju_ref_db": LatchFile(
            "s3://latch-public/test-data/4318/kaiju_db_plasmids.fmi"
        ),
        "kaiju_ref_nodes": LatchFile("s3://latch-public/test-data/4318/nodes.dmp"),
        "kaiju_ref_names": LatchFile("s3://latch-public/test-data/4318/names.dmp"),
        "sample_name": "SRR579292",
        "taxon_rank": TaxonRank.species,
        "min_count": 2,
        "k_min": 21,
        "k_max": 141,
        "k_step": 12,
        "min_contig_len": 200,
        "prodigal_output_format": ProdigalOutput.gff,
        "fargene_hmm_model": fARGeneModel.class_b_1_2,
    },
)
