import math
import time

class alarm:

    piority = [
        {'ilosc_piskow_na_sekunde': 1, 'powtorzenia': 3, 'przerwa': 10},
        {'ilosc_piskow_na_sekunde': 10, 'powtorzenia': 10, 'przerwa': 5},
    ]

    def __init__(self):
        self.list = []
        self.oldtime = 0
        self.position = 0
        self.old_a = 0

    def add(self, pio):
        if pio> len(self.piority):
            pio = len(self.piority) - 1
        self.list.append(pio)
        self.find_top_alarm()

    def find_top_alarm(self):
        l = self.list
        self.list.sort(reverse=True)
        if l != self.list:
            self.position = 0

    def remove(self, pio):
        try:
            self.list.remove(pio)
        except:
            pass
        self.find_top_alarm()

    def top(self):
        try:
            return self.piority[self.list[0]]
        except:
            return False

    def _make_alarm(self, alarm):
        out = ""
        f = alarm['ilosc_piskow_na_sekunde']
        xmax = math.pi * 2
        xmax = int(round(xmax))
        for i in range(0, xmax * 10):
            # generowanie sygnału sinusoidalnego
            wynik =  math.sin(i * f)
            if wynik > 0:
                wynik = 1
            elif wynik <= 0:
                wynik = 0
            out += str(wynik)
        return out + "x"

    def run(self):
        if not self.top() or time.time() - self.oldtime < 1/(2 * math.pi):
            # czy alarm jest włączony oraz czy upłynął czas od ostatniego wywołania
            return self.old_a
        a = self._make_alarm(self.top())
        self.old_a = a
        return a

a = alarm()
a.add(0)
s=time.time()
while time.time() - s < 3:
    x = a.run()
    print(x)

