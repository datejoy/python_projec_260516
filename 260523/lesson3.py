import random   # random: 內建的 module 或 package

answer = random.randint(1, 100)
count = 0

while True:
    try:
        guess = int(input("請輸入數字："))
        count += 1
        if guess > answer:
            print("大了")
        elif guess < answer:
            print("小了")
        else:
            print("猜對了，正確答案為：", answer)
            print("猜的次數：", count)
            break
    except ValueError:
        print("請輸入整數！")















# def get_user_guess() -> int:
#     while True:
#         guess_text = input("請輸入 1~100 之間的整數：").strip()

#         if not guess_text.isdigit():
#             print("輸入格式錯誤，請輸入數字。")
#             continue

#         guess = int(guess_text)
#         if 1 <= guess <= 100:
#             return guess

#         print("輸入範圍錯誤，請輸入 1 到 100 的整數。")


# def play_guess_number() -> None:
#     secret_number = random.randint(1, 100)
#     attempts = 0

#     print("=== 猜數字遊戲 ===")
#     print("我已經想好一個 1 到 100 之間的數字，請開始猜！")

#     while True:
#         guess = get_user_guess()
#         attempts += 1

#         if guess < secret_number:
#             print("太小了，試試看再大一點。")
#         elif guess > secret_number:
#             print("太大了，試試看再小一點。")
#         else:
#             print(f"恭喜你猜對了！答案是 {secret_number}。你總共猜了 {attempts} 次。")
#             break

