> [< back](../README.md)

## **Program Specification: Veterinary Ration Calculator**

### **1. Overview**

**Name:** `vet-ration-cli`

**Purpose:** To automate the calculation of animal rations using the "Tabular Method", verify nutritional balance against specific standards, and perform quick utility calculations (Pearson Square).

### **2. Data Architecture**

The tool relies on two external CSV files to function, allowing students to update data without changing code.

#### **A. Standards Table (`standards.csv`)**

Defines the nutritional requirements (norms) for specific animal categories.

* **Columns:** `Animal_ID`, `Description`, `ME_Target` (Metabolizable Energy), `CP_Target` (Crude Protein %), `Ca_Target`, `P_Target`, `Lysine_Target` (optional), `Tolerance_Pct`.
* *Example:* `Broiler_Start, "Broiler Chicken 0-3w", 3000, 21, 1.0, 0.45, 1.1, 5`

#### **B. Nutrient Table (`feeds.csv`)**

Defines the composition of available feed ingredients.

* **Columns:** `Feed_ID`, `Name`, `Category` (Energy/Protein/Roughage/Mineral), `ME_per_kg`, `CP_Pct`, `Ca_Pct`, `P_Pct`, `Lysine_Pct`, `Max_Inclusion_Pct`.
* *Example:* `Corn, "Yellow Corn", Energy, 3370, 9, 0.02, 0.28, 0.24, 80`

***

### **3. Command Structure**

The program will use a subcommand structure: `python ration.py [COMMAND] [OPTIONS]`

#### **Command 1: `check` (Primary Function)**

Performs the "Tabular Method" calculation. It takes an animal profile and a proposed list of feeds with quantities, then calculates the total nutrition and compares it to the standard.

**Arguments:**

* `--animal` / `-a`: (Required) The `Animal_ID` from the standards table.
* `--diet` / `-d`: (Required) A comma-separated list of feeds and their percentages/weights. Format: `FeedID:Quantity`.
* `--standards`: Path to standards file (Default: `data/standards.csv`).
* `--feeds`: Path to feeds file (Default: `data/feeds.csv`).

**Example Usage:**

```bash
python ration.py check -a Broiler_Start -d "Corn:60,Soy:30,FishMeal:4,Chalk:1"
```

**Processing Logic (The "7 Stages"):**

1. **Load Data:** Read CSVs; validate that requested `Animal_ID` and `Feed_ID`s exist.
2. **Calculate Totals:** For each nutrient (ME, CP, Ca, P):
    * $\text{Total} = \sum (\text{Qty}_{feed} \times \text{Value}_{feed}) / 100$ (if inputs are %).
3. **Verify Ratios:**
    * Calculate **Ca/P Ratio**: $\text{Total Ca} / \text{Total P}$.
    * Calculate **Energy/Protein Ratio**: $\text{Total ME} / \text{Total CP}$.
4. **Compare vs. Standards:**
    * Check if totals are within the defined `Tolerance_Pct` (e.g., ±5% for poultry ).[1]
5. **Check Constraints:** Warn if any ingredient exceeds its `Max_Inclusion_Pct`.

**Output Display:**

* **Ration Table:** A formatted grid showing each ingredient's contribution to ME, CP, Ca, P.
* **Total vs. Norm:** A comparison row showing "Calculated" vs "Required".
* **Analysis Report:**
    * ✅ **Status:** PASS / FAIL
    * ⚠️ **Warnings:** "Protein is 10% below norm", "Ca/P ratio (0.9) is too low (Target 1.2-3.5)".

***

#### **Command 2: `pearson` (Utility)**

Performs the "Pearson Square Method" to balance two ingredients for a single nutrient.[1]

**Arguments:**

* `--target` / `-t`: The target nutrient value (e.g., 12% CP).
* `--feed1` / `-f1`: Value of the first feed (e.g., 9% Corn).
* `--feed2` / `-f2`: Value of the second feed (e.g., 40% Supplement).

**Example Usage:**

```bash
python ration.py pearson -t 14 -f1 9 -f2 38
```

**Output:**

* Displays the square calculation.
* Returns the precise mixing parts (e.g., "Mix 24 parts Corn with 5 parts Supplement").

***

#### **Command 3: `dilute` (Utility)**

Calculates dilution factors for liquid feeds/solutions.[1]

**Arguments:**

* `--start` / `-s`: Initial concentration %.
* `--target` / `-t`: Target concentration %.

**Example Usage:**

```bash
python ration.py dilute -s 45 -t 12
```

**Output:**

* "Dilution Factor: 3.75. Add 2.75 parts water to 1 part solution."

***

### **4. Error Handling Specifications**

* **Invalid Feed ID:** If a user types `Maize` instead of `Corn`, the program must list available similar IDs (fuzzy match).
* **Sum != 100%:** If the input quantities in `check` mode do not sum to 100 (and the user intended percentages), issue a warning but proceed (calculating as absolute amounts).
* **Division by Zero:** Handle cases where Feed P (Phosphorus) is 0 during Ca/P ratio calculation to prevent crash.

### **5. Implementation Stack**

* **Language:** Python 3.10+
* **Libraries:**
    * `argparse` or `click`: For CLI argument parsing.
    * `pandas`: For efficient CSV reading and tabular operations.
    * `tabulate` or `rich`: For rendering pretty Markdown tables in the terminal.

### **6. Future Extensions (Optional)**

* **`optimize` command:** Uses `scipy.optimize` (Linear Programming) to automatically find the cheapest mix that meets all nutrient constraints, replacing the manual trial-and-error of the Tabular method.

> [< back](../README.md)
