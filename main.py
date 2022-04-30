import math
import time
import threading
import sys

class alarm_generator:

    piority = [
        {'ilosc_piskow_na_sekunde': 1, 'przerwa_impuls': 0, 'powtorzenia': 1, 'przerwa': 1},
        {'ilosc_piskow_na_sekunde': 5, 'przerwa_impuls': 2, 'powtorzenia': 3, 'przerwa': 10},
    ]
    bitrate = 10 # Hz

    def __init__(self):
        self.list = []
        self.old_a = 0
        self.oldlist = []
        self.changed = False

    def _top(self):
        try:
            return self.piority[self.list[0]]
        except:
            return False

    def _gen_sinus(self, alarm, precyzja=10):
        # generowanie sekundy sygnału o danej częstotliwości
        _output = ""
        piski = alarm['ilosc_piskow_na_sekunde']
        if 2 * piski > self.bitrate:
            piski = int(self.bitrate / 2)
        for i in range(int(round(2 * math.pi)) * precyzja):
            wynik =  math.sin(i * piski / precyzja)
            if wynik > 0:
                wynik = 1
            elif wynik <= 0:
                wynik = 0
            _output += str(wynik)
        return _output

    def _gen_silent(self):
        # generowanie sekundy ciszy
        return "0" * self.bitrate

    def _gen_wait(self):
        # generowanie sekundy pauzy
        return "w" * self.bitrate

    def _make_alarm(self, alarm):
        _sek_sin = self._make_cut(self._gen_sinus(alarm))
        _sek_sil = self._gen_silent() * alarm['przerwa_impuls']
        _output = ""
        for i in range(alarm['powtorzenia'] + 1):
            _output += _sek_sin + _sek_sil
        if alarm['powtorzenia'] > 0 and alarm['przerwa_impuls'] > 0:
            _output = _output[:-len(_sek_sil)]
        _output += self._gen_wait() * alarm['przerwa']
        return _output

    def _make_cut(self, alarm):
        # ucinanie wyniku do x bitów
        __tmp = ""
        for i in range(1, len(alarm), int(len(alarm) / self.bitrate)):
            __tmp += alarm[i]
        return __tmp

    def _generate(self):
        a = self._make_alarm(self._top())
        self.old_a = a
        return a

    def _find_top_alarm(self):
        self.list.sort(reverse=True)
        try:
            __old = self.oldlist[0]
        except:
            __old = []
        try:
            __new = self.list[0]
        except:
            __new = []
        if __new != __old:
            self.oldlist = self.list.copy()
            self.changed = True

    def is_changed(self):
        a = self.changed
        self.changed = False
        return a

    def add(self, pio):
        if pio > len(self.piority):
            pio = len(self.piority) - 1
        elif pio < 0:
            pio = 0
        self.list.append(pio)
        self._find_top_alarm()

    def remove(self, pio):
        try:
            self.list.remove(pio)
        except:
            pass
        self._find_top_alarm()

    def run(self):
        if not self._top():
            self.old_a = "w"
            return self.old_a
        a = self._generate()
        return a

class run_alarm:
    def __init__(self, bitrate):
        self.pozycja = 0
        self.alarm = "0"
        self.old_time = 0
        self.bitrate = bitrate

    def _is_time(self):
        if time.time() - self.old_time < 1 / self.bitrate:
            return False
        self.old_time = time.time()
        return True

    def add(self, alarm):
        self.pozycja = 0
        self.alarm = alarm

    def tick(self):
        print("tick")

    def run(self):
        if self._is_time():
            self.tick()

lista = alarm_generator()
alarm = run_alarm(lista.bitrate)
lista.add(0)
s = time.time()
while time.time() - s < 10:
    if round(time.time() - s, 2) == 1.0:
        lista.add(1)
        print('dodano 1')
    if round(time.time() - s, 2) == 3.0:
        lista.remove(1)
        print("usunieto 1")
    if round(time.time() - s, 2) == 5.0:
        print('dodano 0')
        lista.add(0)
    if round(time.time() - s, 2) == 7.0:
        lista.remove(0)
        print("usunieto 0")
    if round(time.time() - s, 2) == 8.0:
        lista.remove(0)
        print("usunieto 0")

    x = lista.run()
    if lista.is_changed():
        print('zmiana')
        # print(len(x), lista.is_changed())
    time.sleep(0.01)
