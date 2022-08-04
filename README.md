# metamage

metamage is a workflow for taxonomic classification, assembly, binning
and annotation of short-read metagenomics datasets. It's composed of:

- MEGAHIT for assembly
- MetaQuast for assembly evaluation
- MetaBAT2 for binning

- Kaiju for taxonomic classification

- Prodigal for protein-coding gene prediction on assembly data.

In the next sections, you can read brief descriptions of
all subworkflows contained within metamage.

---

## MetAssembly

MetAssembly is a workflow for assembly of metagenomics data.
It provides as end results both the assembled contigs, binned contigs
evaluation reports of said assembly.

MetAssembly is a workflow composed of:

- [MEGAHIT](https://github.com/voutcn/megahit) for assembly of input reads
- [Quast](https://github.com/ablab/quast), specifically MetaQuast, for assembly evaluation.
- [MetaBAT2](https://bitbucket.org/berkeleylab/metabat/src/master/) for binning of assemblies

---

## Taxonomic classification with Kaiju

Kaiju performs taxonomic classification of
whole-genome sequencing metagenomics reads.
Reads are assigned to taxa by using a reference database
of protein sequences.
Read more about it [here](https://github.com/bioinformatics-centre/kaiju)

---

## Prodigal

Prodigal is a protein-coding gene predictor for prokaryotic genomes.
Read more about it [here](https://github.com/hyattpd/Prodigal).

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
