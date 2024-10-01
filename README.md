# Dosage-sentitive variants types in human genes

This project uses the Ensembl REST API to retrieve gene IDs, variants types for a given list of human gene names.

For the moment, the list of genes requested is hard-coded in the main function.


### Installation:
```zsh
git clone https://github.com/vitorpavinato/dosage-sensitive-genes-variants.git

poetry install
```

### Usage:
```zsh
streamlit run get_human_variant_effect.py
```
