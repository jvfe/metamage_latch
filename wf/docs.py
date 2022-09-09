from latch.types import LatchAuthor, LatchMetadata, LatchParameter

metamage_DOCS = LatchMetadata(
    display_name="MetaMage",
    documentation="https://github.com/jvfe/metamage_latch/blob/main/README.md",
    author=LatchAuthor(
        name="jvfe",
        github="https://github.com/jvfe",
    ),
    repository="https://github.com/jvfe/metamage_latch",
    license="MIT",
    tags=["NGS", "metagenomics", "MAG", "taxonomy"],
)

metamage_DOCS.parameters = {
    "sample_name": LatchParameter(
        display_name="Sample name",
        description="Sample name (will define output file names)",
        batch_table_column=True,
        section_title="Samples",
    ),
    "sample": LatchParameter(
        display_name="Sample data",
        description="Paired-end FASTQ files",
        batch_table_column=True,
    ),
    "host_data": LatchParameter(
        display_name="Host genome & Host name",
        description="FASTA file of the host genome & Host name",
        section_title="Host data",
    ),
    "k_min": LatchParameter(
        display_name="Minimum kmer size",
        description="Must be odd and <=255",
        section_title="MEGAHIT parameters",
    ),
    "k_max": LatchParameter(
        display_name="Maximum kmer size",
        description="Must be odd and <=255",
    ),
    "k_step": LatchParameter(
        display_name="Increment of kmer size of each iteration",
        description="Must be even and <=28",
    ),
    "min_count": LatchParameter(
        display_name="Minimum multiplicity for filtering (k_min+1)-mers",
    ),
    "min_contig_len": LatchParameter(
        display_name="Minimum length of contigs to output",
    ),
    "kaiju_ref_db": LatchParameter(
        display_name="Kaiju reference database (FM-index)",
        description="Kaiju reference database '.fmi' file.",
        section_title="Kaiju parameters",
    ),
    "kaiju_ref_nodes": LatchParameter(
        display_name="Kaiju reference database nodes",
        description="Kaiju reference nodes, 'nodes.dmp' file.",
    ),
    "kaiju_ref_names": LatchParameter(
        display_name="Kaiju reference database names",
        description="Kaiju reference taxon names, 'names.dmp' file.",
    ),
    "taxon_rank": LatchParameter(
        display_name="Taxonomic rank (kaiju2table)",
        description="Taxonomic rank for summary table output (kaiju2table).",
    ),
    "prodigal_output_format": LatchParameter(
        display_name="Prodigal output file format",
        description="Specify main output file format (one of gbk, gff or sco).",
        section_title="Functional analysis parameters",
    ),
    "fargene_hmm_model": LatchParameter(
        display_name="fARGene's HMM model",
        description="The Hidden Markov Model that should be used to predict ARGs from the data",
    ),
}
