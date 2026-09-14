import json
import urllib.request
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

# Matplotlib styling for static web graphics
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "sans-serif"]
plt.rcParams["figure.dpi"] = 150
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.alpha"] = 0.3
plt.rcParams["grid.linestyle"] = "--"

DATA_URL = "https://milne-centre.github.io/BioSPEC/search_index.json"

def fetch_and_compute():
    req = urllib.request.urlopen(DATA_URL)
    raw_data = json.loads(req.read().decode("utf-8"))

    exp_anharm, exp_rot = {}, {}

    for entry in raw_data:
        if entry.get("source_type") == "experiment":
            iso = entry.get("isotopologue") or entry.get("formula") or ""
            for mode in entry.get("vibrational_modes") or []:
                mode_id = mode.get("mode_id")
                if mode.get("anharmonic") is not None:
                    exp_anharm[(iso, mode_id)] = mode["anharmonic"]
                rot = mode.get("rotational_constants") or {}
                for const in ["A", "B", "C"]:
                    if rot.get(const) is not None:
                        exp_rot[(iso, mode_id, const)] = rot[const]

    vib_list = defaultdict(list)
    rot_list = defaultdict(list)

    for entry in raw_data:
        if entry.get("source_type") == "computation":
            iso = entry.get("isotopologue") or entry.get("formula") or ""
            meta = entry.get("computation_metadata") or {}
            method = f"{meta.get('method', '')}/{meta.get('basis_set', '')}".strip("/") or "Unknown"

            for mode in entry.get("vibrational_modes") or []:
                mode_id = mode.get("mode_id")
                calc_anh = mode.get("anharmonic")
                if calc_anh is not None and (iso, mode_id) in exp_anharm:
                    exp_val = exp_anharm[(iso, mode_id)]
                    vib_list[method].append(((calc_anh - exp_val) / exp_val) * 100.0)

                rot = mode.get("rotational_constants") or {}
                for const in ["A", "B", "C"]:
                    calc_r = rot.get(const)
                    if calc_r is not None and (iso, mode_id, const) in exp_rot:
                        exp_val = exp_rot[(iso, mode_id, const)]
                        rot_list[method].append(((calc_r - exp_val) / exp_val) * 100.0)

    vib_errors = {m: np.array(errs) for m, errs in vib_list.items()}
    rot_errors = {m: np.array(errs) for m, errs in rot_list.items()}

    return vib_errors, rot_errors

def generate_artifacts():
    vib_errors, rot_errors = fetch_and_compute()
    all_methods = sorted(list(set(vib_errors.keys()) | set(rot_errors.keys())))

    stats = []
    for m in all_methods:
        v_e = vib_errors.get(m, np.array([]))
        r_e = rot_errors.get(m, np.array([]))

        v_medape = float(np.median(np.abs(v_e))) if len(v_e) > 0 else np.nan
        r_medape = float(np.median(np.abs(r_e))) if len(r_e) > 0 else np.nan

        # Composite score: unweighted average of MedAPEs
        if not np.isnan(v_medape) and not np.isnan(r_medape):
            score = 0.5 * v_medape + 0.5 * r_medape
        elif not np.isnan(v_medape):
            score = v_medape
        elif not np.isnan(r_medape):
            score = r_medape
        else:
            score = np.inf

        stats.append({
            "method": m,
            "vib_N": len(v_e),
            "vib_medape": v_medape,
            "rot_N": len(r_e),
            "rot_medape": r_medape,
            "composite_score": score
        })

    stats.sort(key=lambda x: x["composite_score"])

    # 1. Export summary statistics JSON
    with open("summary_stats.json", "w") as f:
        json.dump(stats, f, indent=2)

    # 2. Generate Side-by-Side Boxplots (Vibrational & Rotational)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    valid_vib = {m: errs for m, errs in vib_errors.items() if len(errs) > 0}
    if valid_vib:
        ax1.boxplot(valid_vib.values(), tick_labels=valid_vib.keys())
        ax1.set_xticklabels(valid_vib.keys(), rotation=45, ha="right")
        ax1.set_ylabel("Error (%)")
        ax1.set_title(r"Vibrational Frequencies ($\nu_0$) Percentage Error")

    valid_rot = {m: errs for m, errs in rot_errors.items() if len(errs) > 0}
    if valid_rot:
        ax2.boxplot(valid_rot.values(), tick_labels=valid_rot.keys())
        ax2.set_xticklabels(valid_rot.keys(), rotation=45, ha="right")
        ax2.set_ylabel("Error (%)")
        ax2.set_title(r"Rotational Constants ($A, B, C$) Percentage Error")

    fig.suptitle("BioSPEC Computational Benchmark Performance", fontweight="bold", fontsize=12)
    plt.tight_layout()
    plt.savefig("method_boxplots.png", dpi=150)
    plt.close()

    # 3. Generate Error Histograms for Top 3 Methods
    top_methods = [s["method"] for s in stats[:3]]
    if top_methods:
        fig, axes = plt.subplots(1, len(top_methods), figsize=(4 * len(top_methods), 3.5), squeeze=False)
        for idx, m in enumerate(top_methods):
            ax = axes[0, idx]
            v_errs = vib_errors.get(m, np.array([]))
            r_errs = rot_errors.get(m, np.array([]))
            
            # Combine all percentage errors for the top composite method
            combined_errs = np.concatenate([v_errs, r_errs]) if len(r_errs) > 0 else v_errs
            
            ax.hist(combined_errs, bins=12, color="steelblue", edgecolor="black", alpha=0.7)
            ax.axvline(0, color="black", linestyle="--", linewidth=1)
            
            v_info = f"Vib N={len(v_errs)}" if len(v_errs) > 0 else "Vib N=0"
            r_info = f"Rot N={len(r_errs)}" if len(r_errs) > 0 else "Rot N=0"
            
            ax.set_title(f"{m}\n({v_info}, {r_info})", fontsize=10)
            ax.set_xlabel("Percentage Error (%)")
            ax.set_ylabel("Count")
            
        fig.suptitle("Overall Error Distributions for Top Ranked Methods", fontweight="bold")
        plt.tight_layout()
        plt.savefig("best_method_histograms.png", dpi=150)
        plt.close()

if __name__ == "__main__":
    generate_artifacts()
    print("Benchmark artifacts successfully generated.")
