# Copyright 2025 Nicolas Spijkerman
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

import argparse
import difflib
import os
import sys

import pandas as pd
from tabulate import tabulate

# --- Configuration & Constants ---

DEFAULT_STANDARDS_FILE = 'data/standards.csv'
DEFAULT_FEEDS_FILE = 'data/feeds.csv'


# --- Data Loading & Validation ---

def load_data(standards_path, feeds_path):
    """Loads and verifies the existence of CSV data files."""
    if not os.path.exists(standards_path):
        sys.exit(f"Error: Standards file not found at '{standards_path}'.")
    if not os.path.exists(feeds_path):
        sys.exit(f"Error: Feeds file not found at '{feeds_path}'.")

    try:
        standards = pd.read_csv(standards_path)
        feeds = pd.read_csv(feeds_path)
    except Exception as e:
        sys.exit(f"Error reading CSV files: {e}")

    # normalize IDs to string and lowercase for easier matching
    standards['Animal_ID'] = standards['Animal_ID'].astype(str)
    feeds['Feed_ID'] = feeds['Feed_ID'].astype(str)

    return standards, feeds


def find_similar_id(target, available_ids):
    """Returns a list of similar IDs using fuzzy matching."""
    return difflib.get_close_matches(target, available_ids, n=3, cutoff=0.6)


# --- Command Implementations ---

def cmd_check(args):
    """Implements the 'Tabular Method' check."""
    standards_df, feeds_df = load_data(args.standards, args.feeds)

    # 1. Validate Animal ID
    animal_row = standards_df[standards_df['Animal_ID'] == args.animal]
    if animal_row.empty:
        similar = find_similar_id(args.animal, standards_df['Animal_ID'].tolist())
        msg = f"Error: Animal ID '{args.animal}' not found."
        if similar:
            msg += f" Did you mean: {', '.join(similar)}?"
        sys.exit(msg)

    animal_std = animal_row.iloc[0]

    # 2. Parse Diet String (Format: "FeedID:Qty,FeedID:Qty")
    diet_entries = args.diet.split(',')
    diet_data = []
    total_qty = 0

    for entry in diet_entries:
        try:
            f_id, qty_str = entry.split(':')
            qty = float(qty_str)
        except ValueError:
            sys.exit(f"Error: Invalid diet format '{entry}'. Use 'FeedID:Quantity'.")

        # Validate Feed ID
        feed_row = feeds_df[feeds_df['Feed_ID'] == f_id]
        if feed_row.empty:
            similar = find_similar_id(f_id, feeds_df['Feed_ID'].tolist())
            msg = f"Error: Feed ID '{f_id}' not found."
            if similar:
                msg += f" Did you mean: {', '.join(similar)}?"
            sys.exit(msg)

        feed_data = feed_row.iloc[0]
        diet_data.append({'Feed_ID': feed_data['Feed_ID'], 'Name': feed_data['Name'], 'Qty': qty, 'Data': feed_data})
        total_qty += qty

    # Warning for non-100% totals
    if abs(total_qty - 100.0) > 0.1:
        print(f"⚠️  Warning: Total diet quantity is {total_qty} (expected 100). Calculating as absolute amounts.\n")

    # 3. Calculate Totals & Check Constraints
    results = []
    total_nutrients = {'ME': 0, 'CP': 0, 'Ca': 0, 'P': 0, 'Lysine': 0}

    print(f"### Ration Analysis for: {animal_std['Description']} ###\n")

    table_rows = []

    for item in diet_data:
        f = item['Data']
        q = item['Qty']

        # Max Inclusion Check
        if q > f['Max_Inclusion_Pct']:
            print(f"⚠️  Constraint Warning: {f['Name']} is at {q}% (Max allowed: {f['Max_Inclusion_Pct']}%)")

        # Contribution Calculation (Value * Qty / 100)
        # Assuming standard table units are per kg or %, usually normalized to 100 units of mix
        # If specs imply kg input, formula is Qty * Value. If % input, Qty * Value / 100.
        # The spec says: Sum (Qty * Value) / 100.

        me_contrib = (q * f['ME_per_kg']) / 100
        cp_contrib = (q * f['CP_Pct']) / 100
        ca_contrib = (q * f['Ca_Pct']) / 100
        p_contrib = (q * f['P_Pct']) / 100
        lys_contrib = (q * f['Lysine_Pct']) / 100

        total_nutrients['ME'] += me_contrib
        total_nutrients['CP'] += cp_contrib
        total_nutrients['Ca'] += ca_contrib
        total_nutrients['P'] += p_contrib
        total_nutrients['Lysine'] += lys_contrib

        table_rows.append([f['Name'], f"{q:.1f}", f"{me_contrib:.1f}", f"{cp_contrib:.2f}", f"{ca_contrib:.2f}", f"{p_contrib:.2f}"])

    # 4. Display Ration Table
    headers = ["Feed", "Qty", "ME", "CP", "Ca", "P"]
    print(tabulate(table_rows, headers=headers, tablefmt="simple"))
    print("-" * 60)

    # 5. Verify Ratios
    ca_p_ratio = total_nutrients['Ca'] / total_nutrients['P'] if total_nutrients['P'] > 0 else 0
    me_cp_ratio = total_nutrients['ME'] / total_nutrients['CP'] if total_nutrients['CP'] > 0 else 0

    # 6. Compare vs Standards
    tolerance = animal_std['Tolerance_Pct'] / 100.0

    comparison_data = [["Metabolizable Energy (ME)", total_nutrients['ME'], animal_std['ME_Target']], ["Crude Protein (CP %)", total_nutrients['CP'], animal_std['CP_Target']],
                       ["Calcium (Ca %)", total_nutrients['Ca'], animal_std['Ca_Target']], ["Phosphorus (P %)", total_nutrients['P'], animal_std['P_Target']],
                       ["Lysine (%)", total_nutrients['Lysine'], animal_std.get('Lysine_Target', '-')]]

    comp_rows = []
    overall_status = "PASS"

    for label, calc, target in comparison_data:
        if target == '-' or pd.isna(target):
            status = "N/A"
            comp_rows.append([label, f"{calc:.2f}", "-", status])
            continue

        target = float(target)
        calc = float(calc)

        low = target * (1 - tolerance)
        high = target * (1 + tolerance)

        if low <= calc <= high:
            status = "✅ OK"
        elif calc < low:
            status = f"🔻 LOW ({((calc - target) / target) * 100:.1f}%)"
            overall_status = "FAIL"
        else:
            status = f"🔺 HIGH (+{((calc - target) / target) * 100:.1f}%)"
            overall_status = "FAIL"

        comp_rows.append([label, f"{calc:.2f}", f"{target:.2f}", status])

    print("\n### Nutritional Balance ###")
    print(tabulate(comp_rows, headers=["Nutrient", "Calculated", "Required", "Status"], tablefmt="github"))

    print("\n### Ratios ###")
    print(f"Ca/P Ratio: {ca_p_ratio:.2f} (Target: 1.2 - 3.5) {'✅' if 1.2 <= ca_p_ratio <= 3.5 else '⚠️'}")
    print(f"Energy/Protein Ratio: {me_cp_ratio:.1f}")

    print(f"\nFINAL RESULT: {overall_status}")


def cmd_pearson(args):
    """Implements the Pearson Square Method."""
    target = args.target
    f1 = args.feed1
    f2 = args.feed2

    # Validation
    if not ((f1 <= target <= f2) or (f2 <= target <= f1)):
        sys.exit("Error: Target value must be between the two feed values.")

    diff1 = abs(f2 - target)  # Parts of Feed 1
    diff2 = abs(f1 - target)  # Parts of Feed 2
    total_parts = diff1 + diff2

    pct1 = (diff1 / total_parts) * 100
    pct2 = (diff2 / total_parts) * 100

    print(f"\n### Pearson Square Calculation (Target: {target}) ###")
    print(f"Feed 1 ({f1}): {diff1:.2f} parts ({pct1:.1f}%)")
    print(f"Feed 2 ({f2}): {diff2:.2f} parts ({pct2:.1f}%)")
    print("-" * 30)
    print(f"Mix {diff1:.2f} parts of Feed 1 with {diff2:.2f} parts of Feed 2.")


def cmd_dilute(args):
    """Implements dilution calculation."""
    start = args.start
    target = args.target

    if target >= start:
        sys.exit("Error: Target concentration must be lower than start concentration for dilution.")
    if target <= 0:
        sys.exit("Error: Target cannot be zero.")

    dilution_factor = start / target
    water_parts = dilution_factor - 1

    print(f"\n### Dilution Calculation ###")
    print(f"Start Conc: {start}% | Target Conc: {target}%")
    print(f"Dilution Factor: {dilution_factor:.2f}")
    print("-" * 30)
    print(f"Add {water_parts:.2f} parts of water to 1 part of solution.")


# --- Main Entry Point ---

def main():
    parser = argparse.ArgumentParser(description="Veterinary Ration Calculator CLI")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Subcommand: check
    check_parser = subparsers.add_parser('check', help='Calculate and verify a ration')
    check_parser.add_argument('-a', '--animal', required=True, help='Animal ID from standards table')
    check_parser.add_argument('-d', '--diet', required=True, help='Diet format: "FeedID:Qty,FeedID:Qty"')
    check_parser.add_argument('--standards', default=DEFAULT_STANDARDS_FILE, help='Path to standards CSV')
    check_parser.add_argument('--feeds', default=DEFAULT_FEEDS_FILE, help='Path to feeds CSV')

    # Subcommand: pearson
    pearson_parser = subparsers.add_parser('pearson', help='Pearson Square Method')
    pearson_parser.add_argument('-t', '--target', type=float, required=True, help='Target nutrient value')
    pearson_parser.add_argument('-f1', '--feed1', type=float, required=True, help='Value of feed 1')
    pearson_parser.add_argument('-f2', '--feed2', type=float, required=True, help='Value of feed 2')

    # Subcommand: dilute
    dilute_parser = subparsers.add_parser('dilute', help='Dilution calculator')
    dilute_parser.add_argument('-s', '--start', type=float, required=True, help='Initial concentration %')
    dilute_parser.add_argument('-t', '--target', type=float, required=True, help='Target concentration %')

    args = parser.parse_args()

    if args.command == 'check':
        cmd_check(args)
    elif args.command == 'pearson':
        cmd_pearson(args)
    elif args.command == 'dilute':
        cmd_dilute(args)


if __name__ == '__main__':
    main()
