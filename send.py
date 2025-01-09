import pywhatkit as kit

# Replace with the phone number and message
phone_numbers = [
    "+254717530861", "+254797279255", "+254726124972", # Add more numbers as needed
]
message = "Hello, this is a test message!"

for number in phone_numbers:
    kit.sendwhatmsg_instantly(number, message)
