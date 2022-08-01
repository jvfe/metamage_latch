"""
Taxonomic classification of reads
"""

import subprocess
from pathlib import Path

from latch import large_task, small_task
from latch.types import LatchDir, LatchFile

from .types import TaxonRank


@large_task
def taxonomy_classification_task(
    read_dir: LatchDir,
    kaiju_ref_nodes: LatchFile,
    kaiju_ref_db: LatchFile,
    sample: str,
) -> LatchFile:
    """Classify metagenomic reads with Kaiju"""

    # Read files
    read1 = Path(read_dir.local_path, f"{sample}_unaligned.fastq.1.gz")
    read2 = Path(read_dir.local_path, f"{sample}_unaligned.fastq.2.gz")

    output_name = f"{sample}_kaiju.out"
    kaiju_out = Path(output_name).resolve()

    _kaiju_cmd = [
        "kaiju",
        "-t",
        kaiju_ref_nodes.local_path,
        "-f",
        kaiju_ref_db.local_path,
        "-i",
        str(read1),
        "-j",
        str(read2),
        "-z",
        "2",
        "-o",
        str(kaiju_out),
    ]

    subprocess.run(_kaiju_cmd)

    return LatchFile(str(kaiju_out), f"latch:///maggie/{sample}/kaiju/{output_name}")


@small_task
def kaiju2table_task(
    kaiju_out: LatchFile,
    kaiju_ref_nodes: LatchFile,
    kaiju_ref_names: LatchFile,
    sample: str,
    taxon: TaxonRank,
) -> LatchFile:
    """Convert Kaiju output to TSV format"""

    output_name = f"{sample}_kaiju.tsv"
    kaijutable_tsv = Path(output_name).resolve()

    _kaiju2table_cmd = [
        "kaiju2table",
        "-t",
        kaiju_ref_nodes.local_path,
        "-n",
        kaiju_ref_names.local_path,
        "-r",
        taxon.value,
        "-p",
        "-e",
        "-o",
        str(kaijutable_tsv),
        kaiju_out.local_path,
    ]

    subprocess.run(_kaiju2table_cmd)

    return LatchFile(
        str(kaijutable_tsv), f"latch:///maggie/{sample}/kaiju/{output_name}"
    )


@small_task
def kaiju2krona_task(
    kaiju_out: LatchFile,
    kaiju_ref_nodes: LatchFile,
    kaiju_ref_names: LatchFile,
    sample: str,
) -> LatchFile:
    """Convert Kaiju output to Krona-readable format"""

    output_name = f"{sample}_kaiju2krona.out"
    krona_txt = Path(output_name).resolve()

    _kaiju2krona_cmd = [
        "kaiju2krona",
        "-t",
        kaiju_ref_nodes.local_path,
        "-n",
        kaiju_ref_names.local_path,
        "-i",
        kaiju_out.local_path,
        "-o",
        str(krona_txt),
    ]

    subprocess.run(_kaiju2krona_cmd)

    return LatchFile(str(krona_txt), f"latch:///maggie/{sample}/kaiju/{output_name}")


@small_task
def plot_krona_task(krona_txt: LatchFile, sample: str) -> LatchFile:
    """Make Krona plot from Kaiju results"""
    output_name = f"{sample}_krona.html"
    krona_html = Path(output_name).resolve()

    _kaiju2krona_cmd = ["ktImportText", "-o", str(krona_html), krona_txt.local_path]

    subprocess.run(_kaiju2krona_cmd)

    return LatchFile(str(krona_html), f"latch:///maggie/{sample}/kaiju/{output_name}")
