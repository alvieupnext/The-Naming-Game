import pandas as pd

part1 = pd.read_csv("output/convergenceMultiHPCPatients.csv", index_col=0)

part2 = pd.read_csv("output/convergenceMultiHPCPatients2.csv", index_col=0)

merged = pd.concat([part1, part2], ignore_index=True)

print(merged)