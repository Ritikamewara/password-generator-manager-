import random
import string

def simple_password(length):
    chars = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(chars) for _ in range(length))


def strong_password(length):
    if length < 4:
        return "❌ Length must be at least 4"

    password = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice(string.punctuation)
    ]

    all_chars = string.ascii_letters + string.digits + string.punctuation
    password += [random.choice(all_chars) for _ in range(length - 4)]

    random.shuffle(password)
    return "".join(password)


def main():
    print("🔐 PASSWORD GENERATOR")
    print("1. Simple Password")
    print("2. Strong Password")

    choice = input("Choose option: ")
    length = int(input("Enter length: "))

    if choice == "1":
        print("Password:", simple_password(length))
    elif choice == "2":
        print("Strong Password:", strong_password(length))
    else:
        print("❌ Invalid choice")


if __name__ == "__main__":
    main()