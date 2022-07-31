from enum import Enum


class TaxonRank(Enum):
    superkingdom = "superkingdom"
    phylum = "phylum"
    taxon_class = "class"
    order = "order"
    family = "family"
    genus = "genus"
    species = "species"


class ProdigalOutput(Enum):
    gbk = "gbk"
    gff = "gff"
    sco = "sco"
