import csv
import datasets

logger = datasets.logging.get_logger(__name__)

_CITATION = """\
@article{OLSON20142643,
title = {A Comprehensive Biophysical Description of Pairwise Epistasis throughout an Entire Protein Domain},
journal = {Current Biology},
volume = {24},
number = {22},
pages = {2643-2651},
year = {2014},
issn = {0960-9822},
doi = {https://doi.org/10.1016/j.cub.2014.09.072},
url = {https://www.sciencedirect.com/science/article/pii/S0960982214012688},
author = {C. Anders Olson and Nicholas C. Wu and Ren Sun},
}
"""

_DESCRIPTION = """\
Summary \
Background \
Nonadditivity in fitness effects from two or more mutations, termed epistasis, can result in compensation of deleterious mutations or negation of beneficial mutations. Recent evidence shows the importance of epistasis in individual evolutionary pathways. However, an unresolved question in molecular evolution is how often and how significantly fitness effects change in alternative genetic backgrounds. \
Results \
To answer this question, we quantified the effects of all single mutations and double mutations between all positions in the IgG-binding domain of protein G (GB1). By observing the first two steps of all possible evolutionary pathways using this fitness profile, we were able to characterize the extent and magnitude of pairwise epistasis throughout an entire protein molecule. Furthermore, we developed a novel approach to quantitatively determine the effects of single mutations on structural stability (ΔΔGU). This enabled determination of the importance of stability effects in functional epistasis. \
Conclusions \
Our results illustrate common biophysical mechanisms for occurrences of positive and negative epistasis. Our results show pervasive positive epistasis within a conformationally dynamic network of residues. The stability analysis shows that significant negative epistasis, which is more common than positive epistasis, mostly occurs between combinations of destabilizing mutations. Furthermore, we show that although significant positive epistasis is rare, many deleterious mutations are beneficial in at least one alternative mutational background. The distribution of conditionally beneficial mutations throughout the domain demonstrates that the functional portion of sequence space can be significantly expanded by epistasis. \
"""

class GB1Config(datasets.BuilderConfig):
    """BuilderConfig for GB1."""

    def __init__(self, **kwargs):
        """BuilderConfig for GB1.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(GB1Config, self).__init__(**kwargs)

class GB1(datasets.GeneratorBasedBuilder):

    BUILDER_CONFIGS = [
        GB1Config(
            name="full_dataset",
            version=datasets.Version("1.0.0", ""),
            description="Full dataset",
        ),
    ]
    
    def variant_to_sequence(self, variant_notation, wild_type_sequence):
        full_sequence = list(wild_type_sequence)
        variants = variant_notation.split(',')
        for variant in variants:
            position, amino_acid = variant[:-1], variant[-1]
            position = int(position[1:])
            full_sequence[position] = amino_acid
        return ''.join(full_sequence)

    def _split_generators(self, dl_manager):
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"filepath": "/content/GB1/train/train.tsv"}
            ),
            datasets.SplitGenerator(
name=datasets.Split.TEST, gen_kwargs={"filepath": "/content/GB1/test/test.tsv"}
            )
        ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "variant": datasets.Value("string"),
                    "seq": datasets.Value("string"),
                    "num_mutations": datasets.Value("int32"),
                    "labels": datasets.Value("float32"),
                }
            ),
            # No default supervised_keys (as we have to pass both question
            # and context as input).
            supervised_keys=None,
            homepage="https://github.com/gitter-lab/nn4dms",
            citation=_CITATION,
            task_templates=[

            ],
        )

    def _generate_examples(self, filepath):
        """This function returns the examples in the raw (text) form."""
        logger.info("generating examples from = %s", filepath)
        wild_type = "MQYKLILNGKTLKGETTTEAVDAATAEKVFKQYANDNGVDGEWTYDDATKTFTVTE"
        with open(filepath, encoding="utf-8") as f:
            reader = csv.reader(f, delimiter='\t')
            for i, row in enumerate(reader):
                if i == 0:
                    continue
                variant, num_mutations, inp, sel, score = row
                seq = self.variant_to_sequence(variant, wild_type)
                yield i, {
                    "variant": variant,
                    "seq": seq,
                    "num_mutations": num_mutations,
                    "labels": float(score)
                }
