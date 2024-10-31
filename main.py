import threading
from random import randint
import time

class Bank:
    def __init__(self, count:int=100):
        self.balance = 0
        self.lock = threading.Lock()
        self.count = count

    def deposit(self):
        for i in range(self.count):
            sum_ = randint(50, 500)
            self.balance += sum_
            print(f'Пополнение: {sum_}. Баланс: {self.balance}')
            time.sleep(0.001)

            if self.balance >= 500:
                if self.lock.locked():
                    self.lock.release()

    def take(self):
        for i in range(self.count):
            sum_ = randint(50, 500)
            print(f'Запрос на {sum_}')

            if sum_ <= self.balance:
                self.balance -= sum_
                print(f'Снятие: {sum_}. Баланс: {self.balance}')
            else:
                print(f'Запрос отклонён, недостаточно средств')
                if not self.lock.locked():
                    self.lock.acquire()

            time.sleep(0.001)



if __name__ == '__main__':
    bk = Bank()
    thread1 = threading.Thread(target=Bank.deposit, args=(bk,))
    thread2 = threading.Thread(target=Bank.take, args=(bk,))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    print(f'Итоговый баланс: {bk.balance}')