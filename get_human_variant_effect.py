"""
Get human variant effect for a list of genes from Ensembl REST API.
"""

import asyncio
import os
import sys
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))
from fetch_endpoint import JSONObject, fetch_endpoint


# Function to get the gene id for a given human gene name:
async def get_human_gene_id(gene_name: str, content_type: str) -> str:
    base_url = "https://rest.ensembl.org/"
    endpoint = f"lookup/symbol/homo_sapiens/{gene_name}?"
    gene = await fetch_endpoint(base_url, endpoint, content_type)
    # return str(gene["id"])
    return (gene_name, str(gene["id"]))


def count_functional_variants(variants: list[dict]) -> tuple[int, int, int]:
    # Initialize the counters
    intron_count = 0
    synonymous_count = 0
    missense_count = 0

    for variant in variants:
        if variant["consequence_type"] == "missense_variant":
            missense_count += 1
        elif variant["consequence_type"] == "synonymous_variant":
            synonymous_count += 1
        elif variant["consequence_type"] == "intron_variant":
            intron_count += 1

    return (intron_count, synonymous_count, missense_count)


# Function to get the variants and effect for a given gene id:
async def get_human_gene_variants(gene: str, content_type: str) -> str:
    base_url = "https://rest.ensembl.org/"
    endpoint = f"/overlap/id/{gene[1]}?feature=variation"
    variants = await fetch_endpoint(base_url, endpoint, content_type)
    variant_counts = count_functional_variants(variants)

    return [
        gene[0],
        gene[1],
        variant_counts[0],
        variant_counts[1],
        variant_counts[2],
        variant_counts[1] / variant_counts[0],
        variant_counts[2] / variant_counts[0],
    ]


async def main() -> None:

    # Multiple genes request
    content_type = "application/json"
    # gene_names = ["ESPN"]
    gene_names = ["ESPN", "BRAF", "PRR29-AS1", "PRR29", "ICAM2", "BRCA2"]

    # Apply the function with asyncio.gather for concurrent calls
    geneids_async = await asyncio.gather(*[get_human_gene_id(gene, content_type) for gene in gene_names])
    print(f"{geneids_async} from asynchronous calls")

    # From the gene ids, apply the function with asyncio.gather for concurrent calls
    gene_variants = await asyncio.gather(*[get_human_gene_variants(gene, content_type) for gene in geneids_async])
    print(gene_variants)

    # Create a dataframe
    df = pd.DataFrame(
        data = gene_variants,
        columns = [
            "gene_name", 
            "gene_id", 
            "intron_count", 
            "synonymous_count", 
            "missense_count", 
            "synonymous_to_intron", 
            "missense_to_intron"
            ])

    # Plot the results
    # df.plot(x="gene_name", y=["intron_count", "synonymous_count", "missense_count"], kind="barh")
    # plt.show()

    st.write("""
    # Human Variant Effect
    How many variants are there in dosage-sensitivet human genes?
    """)

    # Barplot of the results
    fig, ax = plt.subplots()
    ax.barh(df["gene_name"], df["intron_count"], label="intron")
    ax.barh(df["gene_name"], df["synonymous_count"], left=df["intron_count"], label="synonymous")
    ax.barh(df["gene_name"], df["missense_count"], left=df["intron_count"] + df["synonymous_count"], label="missense")
    ax.set_xlabel("Number of variants")
    ax.legend()
    st.pyplot(fig)


if __name__ == "__main__":
    asyncio.run(main())
