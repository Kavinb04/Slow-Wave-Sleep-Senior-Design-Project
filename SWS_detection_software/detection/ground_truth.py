import mne

psg_file = "SC4001E0-PSG.edf"
hyp_file = "SC4001EC-Hypnogram.edf"

raw = mne.io.read_raw_edf(psg_file, preload=False)
annot = mne.read_annotations(hyp_file)
raw.set_annotations(annot)

# --- Time window (in seconds) ---
start_sec = 8*3600
end_sec   = 9*3600 # 9 hrs 9*60*60  

labels = annot.description
onsets = annot.onset

count_s3 = 0
count_s4 = 0

total = len(labels)
for i, (onset, label) in enumerate(zip(onsets, labels)):
    # Progress bar
    pct = (i + 1) / total * 100
    bar = "█" * int(pct // 5) + "-" * (20 - int(pct // 5))
    print(f"\r  Processing... [{bar}] {pct:.1f}%", end="", flush=True)

    if end_sec is not None and (onset < start_sec or onset > end_sec):
        continue
    if "Sleep stage 3" in label:
        count_s3 += 1
    if "Sleep stage 4" in label:
        count_s4 += 1

print()  # newline after progress bar

total_sws = count_s3 + count_s4

print(f"Time window    : {start_sec//3600}h to {end_sec//3600}h")
print(f"Stage 3 epochs : {count_s3}")
print(f"Stage 4 epochs : {count_s4}")
print(f"Total SWS      : {total_sws}  ({total_sws * 30 / 60:.1f} min)")