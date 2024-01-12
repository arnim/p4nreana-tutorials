import pandas as pd
import matplotlib.pyplot as plt

# Read the result of 2 Gaia queries with pandas

table1 = pd.read_csv('gaia_table_1.csv')
table2 = pd.read_csv('gaia_table_2.csv')

# Find common objects

table_match = pd.merge(table1, table2, on='source_id')

# Save plot of the results

fig, ax = plt.subplots(1,1, figsize=(7,5))

ax.plot(table1.ra, table1.dec, '.', label='Table 1')
ax.plot(table2.ra, table2.dec, '.', label='Table 2')
ax.plot(table_match.ra_x, table_match.dec_x, 'o', mfc='None', label='Match')
ax.invert_xaxis()
ax.set_xlabel('RA')
ax.set_ylabel('Dec')
ax.legend()

fig.tight_layout()
plt.savefig('results/table_match.png', format='png', dpi=150)

# Save the results in a new table

table_match.to_csv('results/table_match.csv', index=False)
