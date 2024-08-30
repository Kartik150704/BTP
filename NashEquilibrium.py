import numpy as np
import nashpy as nash

# Get input from the user
num_attackers = int(input("Enter the number of attackers: "))
num_defenders = int(input("Enter the number of defenders: "))

# 1. Define the Functional Dependency and Topological Dependency Matrices
num_vulnerabilities = max(num_attackers, num_defenders)
W_adj = np.random.randint(0, 2, (num_vulnerabilities, num_vulnerabilities))
N_topology = np.random.randint(0, 2, (num_vulnerabilities, num_vulnerabilities))

# 2. Compute Dependency Scores
S_FunDep = np.sum(W_adj, axis=1)
S_TDep = np.sum(N_topology, axis=1)

# Define weights
w1 = 0.5
w2 = 0.5

# Compute Risk Scores
R_adj = w1 * S_FunDep + w2 * S_TDep

# 3. Example Vulnerability Data
vulnerabilities = {
    f"v{i}": {
        "CA_v": np.random.randint(1, 10),
        "CD_v": np.random.randint(1, 10),
        "IA_v": np.random.randint(1, 10),
        "PrA_v": np.random.randint(1, 10),
    }
    for i in range(1, num_vulnerabilities + 1)
}

# 4. Compute Attack and Defense Costs
def calculate_costs(vul):
    ESC = 1  # Example value
    Vul_exploit = 1  # Example value
    k4 = 1  # Example value
    k5 = 1  # Example value
    CD = k4 * ESC + k5 * Vul_exploit
    IA = vulnerabilities[vul]["IA_v"]
    CA = vulnerabilities[vul]["CA_v"]
    return CD, IA, CA

# 5. Define Payoff Matrices for Attackers and Defenders
payoff_matrix_attacker = np.zeros((num_attackers, num_defenders))
payoff_matrix_defender = np.zeros((num_defenders, num_attackers))

# Populate matrices with calculated costs
for attacker in range(num_attackers):
    for defender in range(num_defenders):
        vuln = f"v{(attacker + defender) % num_vulnerabilities + 1}"
        CD, IA, CA = calculate_costs(vuln)

        # Adjust values according to your payoff structure
        payoff_matrix_attacker[attacker, defender] = IA - CD
        payoff_matrix_defender[defender, attacker] = CA - CD

# Create the game using nashpy
game = nash.Game(payoff_matrix_attacker, payoff_matrix_defender)

# Function to print matrices with row and column descriptions
def print_matrix_with_description(matrix, title, row_desc, col_desc):
    print(f"\n{title}")
    print("-" * 50)
    
    # Print column headers
    print("        ", end="")
    for j in range(len(col_desc)):
        print(f"{col_desc[j]:>7}", end=" ")
    print()
    
    # Print rows with row headers
    for i, row in enumerate(matrix):
        print(f"{row_desc[i]:<7}", end=" ")
        print(" ".join(f"{x:7.2f}" for x in row))

# Function to print vector with description
def print_vector_with_description(vector, title, row_desc):
    print(f"\n{title}")
    print("-" * 50)
    for i, value in enumerate(vector):
        print(f"{row_desc[i]:<7} {value:7.2f}")

# Create row and column descriptions
vuln_desc = [f"v_{i+1}" for i in range(num_vulnerabilities)]
attacker_desc = [f"Att_{i+1}" for i in range(num_attackers)]
defender_desc = [f"Def_{i+1}" for i in range(num_defenders)]

# Print all matrices
print_matrix_with_description(W_adj, "Functional Dependency Matrix (W_adj)", vuln_desc, vuln_desc)
print_matrix_with_description(N_topology, "Topological Dependency Matrix (N_topology)", vuln_desc, vuln_desc)
print_vector_with_description(S_FunDep, "Functional Dependency Scores (S_FunDep)", vuln_desc)
print_vector_with_description(S_TDep, "Topological Dependency Scores (S_TDep)", vuln_desc)
print_vector_with_description(R_adj, "Risk Scores (R_adj)", vuln_desc)

print("\nVulnerability Data:")
for vuln, data in vulnerabilities.items():
    print(f"{vuln}: {data}")

print_matrix_with_description(payoff_matrix_attacker, "Attacker's Payoff Matrix", attacker_desc, defender_desc)
print_matrix_with_description(payoff_matrix_defender, "Defender's Payoff Matrix", defender_desc, attacker_desc)

# Compute Nash equilibria
equilibria = list(game.support_enumeration())

# Print the equilibria
print("\nNash Equilibria:")
for i, eq in enumerate(equilibria, 1):
    print(f"\nEquilibrium {i}:")
    print("Attacker's strategy:", eq[0])
    print("Defender's strategy:", eq[1])

# Add descriptions of the payoff matrices
print("\nDescription of Matrices:")
print("1. Functional Dependency Matrix (W_adj):")
print("   - Shows the functional dependencies between vulnerabilities")
print("   - A value of 1 indicates a dependency, 0 indicates no dependency")

print("\n2. Topological Dependency Matrix (N_topology):")
print("   - Shows the topological dependencies between vulnerabilities")
print("   - A value of 1 indicates a dependency, 0 indicates no dependency")

print("\n3. Functional Dependency Scores (S_FunDep):")
print("   - Sum of functional dependencies for each vulnerability")

print("\n4. Topological Dependency Scores (S_TDep):")
print("   - Sum of topological dependencies for each vulnerability")

print("\n5. Risk Scores (R_adj):")
print("   - Combined risk score for each vulnerability")
print("   - Calculated as: R_adj = w1 * S_FunDep + w2 * S_TDep")

print("\n6. Vulnerability Data:")
print("   - CA_v: Cost of Attack for each vulnerability")
print("   - CD_v: Cost of Defense for each vulnerability")
print("   - IA_v: Impact of Attack for each vulnerability")
print("   - PrA_v: Probability of Attack for each vulnerability")

print("\n7. Attacker's Payoff Matrix:")
print("   - Rows represent different attackers (Att_1, Att_2, ...)")
print("   - Columns represent different defenders (Def_1, Def_2, ...)")
print("   - Each cell (i,j) represents the payoff for attacker i when facing defender j")
print("   - Payoff = Impact of Attack (IA) - Cost of Attack (CD)")

print("\n8. Defender's Payoff Matrix:")
print("   - Rows represent different defenders (Def_1, Def_2, ...)")
print("   - Columns represent different attackers (Att_1, Att_2, ...)")
print("   - Each cell (i,j) represents the payoff for defender i when facing attacker j")
print("   - Payoff = Cost of Attack (CA) - Cost of Defense (CD)")

print("\nNote: Higher values in the payoff matrices are better for the respective player.")