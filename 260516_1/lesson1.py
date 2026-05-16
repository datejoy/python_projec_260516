import random


def get_user_guess() -> int:
    while True:
        guess_text = input("請輸入 1~100 之間的整數：").strip()

        if not guess_text.isdigit():
            print("輸入格式錯誤，請輸入數字。")
            continue

        guess = int(guess_text)
        if 1 <= guess <= 100:
            return guess

        print("輸入範圍錯誤，請輸入 1 到 100 的整數。")


def play_guess_number() -> None:
    secret_number = random.randint(1, 100)
    attempts = 0

    print("=== 猜數字遊戲 ===")
    print("我已經想好一個 1 到 100 之間的數字，請開始猜！")

    while True:
        guess = get_user_guess()
        attempts += 1

        if guess < secret_number:
            print("太小了，試試看再大一點。")
        elif guess > secret_number:
            print("太大了，試試看再小一點。")
        else:
            print(f"恭喜你猜對了！答案是 {secret_number}。你總共猜了 {attempts} 次。")
            break


def main() -> None:
    while True:
        play_guess_number()
        again = input("再玩一次嗎？輸入 y 繼續，或按其他任意鍵結束：").strip().lower()
        if again != "y":
            print("感謝遊玩，再見！")
            break


if __name__ == "__main__":
    main()
