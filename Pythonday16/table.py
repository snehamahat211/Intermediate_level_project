from prettytable import PrettyTable
table=PrettyTable()
table.field_names=["Number","Multiplier","result"]
for i in range(1,11):
    table.add_row=([5,i,5*i])
print (table)