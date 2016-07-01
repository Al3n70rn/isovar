# Copyright (c) 2016. Mount Sinai School of Medicine
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function, division, absolute_import
from argparse import ArgumentParser

from ..default_parameters import (
    MAX_REFERENCE_TRANSCRIPT_MISMATCHES,
    MIN_TRANSCRIPT_PREFIX_LENGTH,
    CDNA_CONTEXT_SIZE
)
from ..reference_context import variants_to_reference_contexts_dataframe

from .variants import variants_from_args, add_somatic_vcf_args

def add_reference_context_args(parser, add_context_size_arg=True):
    """
    Extends an ArgumentParser instance with the following commandline arguments:
        --max-reference-transcript-mismatches
        --min-transcript-prefix-length
    """
    reference_context_group = parser.add_argument_group("Reference Transcripts")
    reference_context_group.add_argument(
        "--max-reference-transcript-mismatches",
        type=int,
        default=MAX_REFERENCE_TRANSCRIPT_MISMATCHES,
        help=(
            "Maximum number of mismatches between variant sequence"
            " reference sequence before a candidate reading frame is ignored."))

    reference_context_group.add_argument(
        "--min-transcript-prefix-length",
        type=int,
        default=MIN_TRANSCRIPT_PREFIX_LENGTH,
        help=(
            "Number of nucleotides before the variant we try to match against "
            "a reference transcript. Values greater than zero exclude variants "
            "near the start codon of transcrPROTEIN_SEQUENCE_LEGNTHipts without 5' UTRs."))
    if add_context_size_arg:
        parser.add_argument(
            "--context-size",
            default=CDNA_CONTEXT_SIZE,
            type=int)
    return reference_context_group

def make_reference_context_arg_parser(add_context_size_arg=True, **kwargs):
    """
    Parameters
    ----------
    add_context_size_arg : bool
        If True then add a `--context-size` argument, which is otherwise
        inferred from cDNA sequence length.
    **kwargs : dict
        Parameters passed directly to argparse.ArgumentParser.

    Returns an argparse.ArgumentParser instance.
    """
    parser = ArgumentParser(**kwargs)
    add_somatic_vcf_args(parser)
    add_reference_context_args(parser, add_context_size_arg=add_context_size_arg)
    return parser

def reference_contexts_dataframe_from_args(args):
    variants = variants_from_args(args)
    return variants_to_reference_contexts_dataframe(
        variants=variants,
        context_size=args.context_size)
