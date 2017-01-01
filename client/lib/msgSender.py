# -*-coding:Utf-8 -*

from threading import Thread
import time

stop = False  # variable globale servant à stopper les threads.


class MsgSender(Thread):
    def __init__(self, connection):
        Thread.__init__(self)
        self.connection = connection

    def run(self):

        while True:
            global stop
            msg_a_envoyer = input("> \n")
            # Peut planter si vous tapez des caractères spéciaux
            msg_a_envoyer = "|{}|".format(msg_a_envoyer)
            msg_a_envoyer = msg_a_envoyer.encode()

            if stop is False:
                # On envoie le message
                self.connection.send(msg_a_envoyer)

            else:
                break


class StatusSender(Thread):

    def __init__(self, connection):
        Thread.__init__(self)
        self.connection = connection

    def run(self):
        msg_recu = ""
        global stop
        while True:

            if stop is False:
                msg_a_envoyer = "|status|"

                # Peut planter si vous tapez des caractères spéciaux
                msg_a_envoyer = msg_a_envoyer.encode()

                # On envoie le message
                self.connection.send(msg_a_envoyer)
            if stop is True:
                break
            time.sleep(0.05)


class MsgRecever(Thread):

    def __init__(self, connection):
        Thread.__init__(self)
        self.connection = connection

    def run(self):
        msg_recu = ""
        global stop
        while True:
            last_msg = msg_recu
            msg_recu = self.connection.recv(1024)
            msg_recu = msg_recu.decode()
            paquet = msg_recu.split("|")
            last_paquet = last_msg.split("|")

            i = 0
            while i < len(paquet):
                if paquet[i] != "":
                    if paquet[i] not in last_paquet:
                        print(paquet[i])
                        if paquet[i] == "fin":
                            stop = True

                i += 1
            if stop is True:
                break

            time.sleep(0.05)
