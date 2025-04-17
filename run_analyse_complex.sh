#!/bin/bash

# === CONFIGURATION ===
FOLDX_CMD="foldx"
INPUT_DIR="Build_model"
OUTPUT_DIR="AnalyseComplex_Results"
NUM_MUTANTS=10
CHAINS="A,L"

mkdir -p "$OUTPUT_DIR"

for i in $(seq 1 $NUM_MUTANTS); do
    echo "🔬 Processing mutant $i..."

    # Input files
    MUT_PDB="${INPUT_DIR}/complex_repaired_${i}.pdb"
    WT_PDB="${INPUT_DIR}/WT_complex_repaired_${i}.pdb"

    # Check both exist
    if [[ ! -f "$MUT_PDB" || ! -f "$WT_PDB" ]]; then
        echo "⚠️  Skipping mutant $i (missing PDB file)"
        continue
    fi

    # --- Mutant Run ---
    cp "$MUT_PDB" .
    $FOLDX_CMD --command=AnalyseComplex \
               --pdb="$(basename "$MUT_PDB")" \
               --analyseComplexChains="$CHAINS" \
               --complexWithDNA=false
    rm "$(basename "$MUT_PDB")"

    # --- WT Run ---
    cp "$WT_PDB" .
    $FOLDX_CMD --command=AnalyseComplex \
               --pdb="$(basename "$WT_PDB")" \
               --analyseComplexChains="$CHAINS" \
               --complexWithDNA=false
    rm "$(basename "$WT_PDB")"

    # Move default-named output files to result folder
    mv Interaction_*.fxout "$OUTPUT_DIR/" 2>/dev/null
    mv Summary_*.fxout "$OUTPUT_DIR/" 2>/dev/null
    mv Indiv_energies_*.fxout "$OUTPUT_DIR/" 2>/dev/null
    mv Interface_Residues_*.fxout "$OUTPUT_DIR/" 2>/dev/null

    echo "✅ Done with mutant $i"
done

echo -e "\n🎉 All finished. Output files moved to: $OUTPUT_DIR"

