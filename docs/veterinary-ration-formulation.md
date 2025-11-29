> [< back](../README.md)

## **Veterinary Ration Formulation**

### **I. Introduction**

**Objective:** Able to design, calculate, and verify a balanced diet for livestock (pigs, poultry, and herbivores) using standard nutritional tables and manual calculation techniques.

**Core Concept:** Ration balancing is the process of matching the nutrient content of available feeds (fodder, grains, supplements) with the nutrient requirements (feeding norms) of a specific animal to ensure health, growth, and production efficiency.

***

### **II. Theoretical Foundations**

#### **A. The 7 Stages of Ration Elaboration**

Ration formulation follows a systematic process to ensure precision and safety.

1. **Determine Standards:** Identify the nutrient requirements (feeding norms) for the specific animal type, age, and production level.
2. **Establish Fodder List:** Select appropriate feeds based on species physiology:
    * **Pig & Poultry:** Primarily concentrated feeds.
    * **Herbivores:** Must include bulky forages (Succulent/Silage and Fibrous/Roughage).
3. **Determine Proportions:** Set inclusion rates (% or kg) for each ingredient, respecting maximum limits (e.g., salt, fish meal).
4. **Establish Nutritive Value (NV):** Retrieve nutrient data (Energy, Protein, Calcium, Phosphorus, etc.) from standard tables.
5. **Calculate NV in Diet:** Multiply the quantity of each feed by its nutrient density.
6. **Sum Partial Sums:** Total the nutrients provided by all ingredients.
7. **Compare & Adjust:** Compare the total supplied nutrients against the standards (step 1) and adjust as necessary.

#### **B. Rules & Tolerances**

Precision is critical, but biological systems allow for slight deviations.

* **Tolerances:**
    * **Herbivores:** ±10% deviation from standards is acceptable.
    * **Pigs & Poultry:** Stricter tolerance of ±5%.
* **Ratios to Monitor:**
    * **Protein Ratio:** Critical for herbivores.
    * **Energy-Protein (E-P) Ratio:** Essential for pigs and poultry.
    * **Ca/P Ratio:** Critical for all diets (Target ~1-3:1; can reach 3.5:1 for some).

***

### **III. Feed Selection Guidelines**

#### **A. Poultry Ration Rules**

* **Energy Sources:**
    * **Corn:** Mandatory! Inclusion 50–80%.
    * **Wheat:** 10–40%.
    * **Animal Fat:** Max 2–5%.
* **Protein Sources:**
    * **Soybean Meal:** 10–20%.
    * **Fish Meal:** Max 3–5% (Avoid in laying hens to prevent "fishy" eggs).
* **Minerals:**
    * **Ca+P:** 1–3% (Higher for laying hens).
    * **Zoofort:** Always 1%.

#### **B. Pig Ration Rules**

* **Energy Sources:**
    * **Corn:** 30–80% (Highly advised).
    * **Animal Fat:** 3–5% max.
* **Protein Sources:**
    * **Soybean Meal:** 10–25%.
    * **Fish Meal / Yeast:** 3–5% max.
    * **Powdered Milk:** 5–20% (Higher for young piglets).
* **Critical Amino Acid:** Lysine is the limiting amino acid for pigs.

***

### **IV. Calculation Methodologies**

#### **A. The Tabular Method (Grid Calculation)**

This is the standard "Exploratory" method used in your worksheets.

1. **Create a Grid:** Columns for Quantity, Metabolizable Energy (ME), Crude Protein (CP), Calcium (Ca), Phosphorus (P), etc.
2. **Input Norms:** Write the daily requirements in the top row (e.g., ME=3100, CP=17%).
3. **Draft Quantities:** Assign tentative percentages to feeds (e.g., Corn 60%, Soy 20%).
4. **Calculate Contributions:**
   $$\text{Nutrient Supplied} = \frac{\text{Feed \%} \times \text{Nutrient Value per kg}}{100}$$
    * *Example:* If Corn has 3370 ME and is 60% of the diet: $0.60 \times 3370 = 2022 \text{ME}$.
5. **Sum and Check:** Add up all columns. If the total CP is 15%, but you need 17%, increase protein sources (Soy/Fish meal) and decrease energy sources (Corn) slightly.

#### **B. The Pearson Square Method**

Use this to balance *one* specific nutrient (usually Protein) using *two* ingredients (or mixtures).

* **Scenario:** You need a 12% protein mix using Corn (9% CP) and Supplement (40% CP).
* **Setup:**
    1. Draw a square. Put target (12) in the center.
    2. Put source values on left corners (40 top, 9 bottom).
    3. Subtract diagonally:
        * $40 - 12 = 28$ parts Corn.
        * $12 - 9 = 3$ parts Supplement.
    4. **Result:** Mix 28 parts Corn with 3 parts Supplement.

#### **C. Volume/Concentration Mixing**

Used when diluting solutions or mixing liquid feeds.

* **Formula:** $C_1V_1 + C_2V_2 = C_{final}V_{final}$
* *Example from cards:* Mixing a 45% solution and 0% solution to get 12%.
    * $D_f = \frac{Concentration_{start}}{Concentration_{target}} = \frac{45}{12} = 3.75$.
    * You dilute the source 3.75 times.

***

### **V. Verification & Quality Control**

Once the ration is calculated, you must verify the ratios.

#### **1. Calcium-Phosphorus Ratio ($R_{Ca/P}$)**

* **Formula:** $R_{Ca/P} = \frac{\text{Total Ca in Diet}}{\text{Total P in Diet}}$
* **Check:** value must fall within the norm (typically 1.2–3.5 depending on species).
* **Tolerance:** Ensure the result is within ±5% of the target ratio.
    * *Example:* If target is 1.25, acceptable range is $1.18 - 1.31$.

#### **2. Energy-Protein Ratio ($R_{ME/CP}$)**

* **Formula:** $R_{ME/CP} = \frac{\text{Total Metabolizable Energy}}{\text{Total Crude Protein}}$
* **Check:** Compare calculated ratio vs. standard ratio.
    * *Example:* Standard $3200/11 = 290.9$. Calculated $288.3$.
    * **Conclusion:** "Good, in norms".

#### **3. Correction Logic**

* **Too much Protein?** Reduce protein-rich feeds (Soy, Fish meal) and increase energy feeds (Corn).
* **Too much Energy?** Reduce Corn/Fat, increase fibrous feeds (Bran, Alfalfa) or lower-energy grains (Oats).
* **Fiber limit exceeded?** Remove fibrous ingredients (Sunflower meal, Bran) and replace with concentrated sources (Soy, Corn).
* **Mineral Imbalance?** Adjust specific additives (Carb Ca, Dicalcium Phosphate) without altering the main energy/protein sources.

> [< back](../README.md)
