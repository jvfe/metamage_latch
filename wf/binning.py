import subprocess
from pathlib import Path

from latch import large_task, small_task, workflow
from latch.types import LatchDir, LatchFile


@large_task
def bowtie_assembly_build(assembly_dir: LatchDir, sample_name: str) -> LatchDir:

    assembly_name = f"{sample_name}.contigs.fa"
    assembly_fasta = Path(assembly_dir.local_path, assembly_name)

    output_dir_name = f"{sample_name}_assembly_idx"
    output_dir = Path(output_dir_name).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    _bt_idx_cmd = [
        "bowtie2/bowtie2-build",
        str(assembly_fasta),
        f"{str(output_dir)}/{sample_name}",
        "--threads",
        "31",
    ]

    subprocess.run(_bt_idx_cmd)

    return LatchDir(
        str(output_dir), f"latch:///metamage/{sample_name}/{output_dir_name}"
    )


@large_task
def bowtie_assembly_align(
    assembly_idx: LatchDir,
    read_dir: LatchDir,
    sample_name: str,
) -> LatchFile:

    # Read files
    read1 = Path(read_dir.local_path, f"{sample_name}_unaligned.fastq.1.gz")
    read2 = Path(read_dir.local_path, f"{sample_name}_unaligned.fastq.2.gz")

    output_file_name = f"{sample_name}_assembly_sorted.bam"

    output_file = Path(output_file_name).resolve()

    _bt_cmd = [
        "bowtie2/bowtie2",
        "-x",
        f"{assembly_idx.local_path}/{sample_name}",
        "-1",
        str(read1),
        "-2",
        str(read2),
        "--threads",
        "31",
    ]

    bt_align_out = subprocess.Popen(
        _bt_cmd,
        stdout=subprocess.PIPE,
    )

    _sam_convert_cmd = [
        "samtools",
        "view",
        "-@",
        "31",
        "-bS",
    ]

    sam_convert_out = subprocess.Popen(
        _sam_convert_cmd, stdin=bt_align_out.stdout, stdout=subprocess.PIPE
    )

    _sam_sort_cmd = [
        "samtools",
        "sort",
        "-@",
        "31",
        "-o",
        output_file_name,
    ]

    subprocess.run(
        _sam_sort_cmd,
        stdin=sam_convert_out.stdout,
    )

    return LatchFile(
        str(output_file), f"latch:///metamage/{sample_name}/{output_file_name}"
    )


@small_task
def summarize_contig_depths(assembly_bam: LatchFile, sample_name: str) -> LatchFile:

    output_file_name = f"{sample_name}_depths.txt"
    output_file = Path(output_file_name).resolve()

    _jgi_cmd = [
        "jgi_summarize_bam_contig_depths",
        "--outputDepth",
        output_file_name,
        assembly_bam.local_path,
    ]

    subprocess.run(_jgi_cmd)

    return LatchFile(
        str(output_file), f"latch:///metamage/{sample_name}/{output_file_name}"
    )


@large_task
def metabat2(
    assembly_dir: LatchDir,
    depth_file: LatchFile,
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
        "-a",
        depth_file.local_path,
        "-o",
        output_dir_name,
    ]

    subprocess.run(_metabat_cmd)

    return LatchDir(str(output_dir), f"latch:///metamage/{sample_name}/METABAT/")


@workflow
def binning_wf(
    read_dir: LatchDir, assembly_dir: LatchDir, sample_name: str
) -> LatchDir:

    # Binning preparation
    built_assembly_idx = bowtie_assembly_build(
        assembly_dir=assembly_dir, sample_name=sample_name
    )
    aligned_to_assembly = bowtie_assembly_align(
        assembly_idx=built_assembly_idx, read_dir=read_dir, sample_name=sample_name
    )
    depth_file = summarize_contig_depths(
        assembly_bam=aligned_to_assembly, sample_name=sample_name
    )

    # Binning
    binning_results = metabat2(
        assembly_dir=assembly_dir, depth_file=depth_file, sample_name=sample_name
    )

    return binning_results
