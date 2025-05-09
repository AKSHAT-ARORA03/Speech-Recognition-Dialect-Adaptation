import os
import pandas as pd
import shutil

# ✅ CONFIGURATION
EN_DIR = "../data/cv-corpus-21.0-delta-2025-03-14-en/cv-corpus-21.0-delta-2025-03-14/en"
CLIPS_DIR = os.path.join(EN_DIR, "clips")
VALIDATED_TSV = os.path.join(EN_DIR, "validated.tsv")
OUTPUT_AUDIO_DIR = "../audio_samples/"
N = 5  # Number of samples to extract

# ✅ Load the TSV file
df = pd.read_csv(VALIDATED_TSV, sep="\t")

# ✅ Drop missing entries
df = df[["path", "sentence"]].dropna().head(N)

# ✅ Create output directory if it doesn't exist
os.makedirs(OUTPUT_AUDIO_DIR, exist_ok=True)

# ✅ Copy audio + save transcripts
with open(os.path.join(OUTPUT_AUDIO_DIR, "transcripts.txt"), "w", encoding="utf-8") as out:
    for _, row in df.iterrows():
        src = os.path.join(CLIPS_DIR, row["path"])
        dst = os.path.join(OUTPUT_AUDIO_DIR, row["path"])
        shutil.copy(src, dst)
        out.write(f"{row['path']}\t{row['sentence']}\n")

print(f"✅ Extracted {len(df)} samples to {OUTPUT_AUDIO_DIR}")
