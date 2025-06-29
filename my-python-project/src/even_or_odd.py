def is_even_or_odd(number):
    if number % 2 == 0:
        return "Even"
    else:
        return "Odd"

if __name__ == "__main__":
    num = int(input("Enter a number: "))
    result = is_even_or_odd(num)
    print(f"The number {num} is {result}.")