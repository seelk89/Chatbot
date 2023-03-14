# File for testing of misc. stuff.

# The below code does not seem to work when applied to GPTNeoGenerator's output.
test_string = 'Yes, we really do like our butts. They’re perfect for you. They’re not much to look at but they’re absolutely the best. Like I said, don’t like butts, butts for everyone. They’re the only kind of butts. Butts that don’t get in the way of the action. There’s just no room to'

last_period_index = test_string.rfind(".")
if last_period_index != -1:
    first_part = test_string[:last_period_index]
    second_part = test_string[last_period_index+1:]
    print(first_part)
else:
    print("String does not contain a period.")
