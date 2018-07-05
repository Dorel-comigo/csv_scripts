import sys

if len(sys.argv) >= 2:
    input_A = sys.argv[1]
else:
    input_A = input("Please enter a number for the relevant query to run: "
                    "\n 1 - SELECT"
                    "\n 2 - INSERT"
                    "\n 3 - UPDATE:")
if input_A == '1':
    if len(sys.argv) >= 3:
        input_B = sys.argv[2]
    else:
        input_B = input("Please enter the name of the requested columns to show:")
print(input_B)
print(len(input_B.split(" ")))








