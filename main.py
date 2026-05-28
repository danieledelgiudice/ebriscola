#! /usr/bin/env python
#! -*- coding:utf-8 -*-
import pygame
import os
import sys
import pygame.locals
from random import randint, randrange
from sprites import SpriteCarta
from time import time


class Carta:
    """
    Definisce una carta da gioco
    """

    elencoSemi = ["Fiori", "Quadri", "Picche", "Cuori"]
    elencoValori = ["", "Asso", "2", "3", "4", "5", "6", "7", "Fante", "Cavallo", "Re"]
    ordineImportanza = [1, 3, 10, 9, 8, 7, 6, 5, 4, 2]

    def __init__(self, seme, valore):
        """
        Crea una carta
        """
        self.seme = seme
        self.valore = valore

    def __gt__(self, altro):
        return self.ordineImportanza.index(self.valore) < self.ordineImportanza.index(
            altro.valore
        )


class Mazzo:
    """
    Definisce un mazzo generico di 40 carte
    """

    def __init__(self):
        """
        Crea un mazzo di 40 carte usando i 4 semi e 10 carte per ogni seme
        """
        self.carte = []
        for seme in range(4):
            for valore in range(1, 11):
                self.carte.append(Carta(seme, valore))
        self.Mescola()

    def Mescola(self):
        """
        Mescola le carte cambiando la posizione di ogni carta con un' altra trovata casualmente
        """
        for i in range(len(self.carte)):
            r = randrange(0, len(self.carte))
            self.carte[i], self.carte[r] = self.carte[r], self.carte[i]

    def Pesca(self):
        """
        Ritorna e rimuove la prima carta
        """
        return self.carte.pop()

    def EVuoto(self):
        """Ritorna true se non ci sono carte"""
        return len(self.carte) == 0

    def PrimaCarta(self):
        """Ritorna e rimuove la prima carta"""
        return self.carte.pop()

    def DistribuisciCarte(self, listaMani, numeroCarte=999):
        """
        Distribuisce numeroCarte carte ai listaGiocatori

        Nota: numCarte e' inteso come numero di carte totali distribuite
        """
        numMani = len(listaMani)
        for n in range(numeroCarte):
            if self.EVuoto():
                break
            carta = self.PrimaCarta()
            mano = listaMani[n % numMani]
            mano.AggiungiCarta(carta)


class Mano(Mazzo):
    """
    Definisce una generica mano da gioco
    """

    def __init__(self):
        """
        Crea una mano con il nome passato per argomento
        """
        self.carte = []

    def AggiungiCarta(self, carta):
        """
        Aggiunge la carta passata per argomento alla mano
        """
        self.carte.append(carta)


class Tavolo:
    """Definisce il tavolo da gioco.

    E' composto da:
    self.carte : carte sul tavolo
    self.briscola: carta di briscola
    self.vincitore: chi ha vinto il turno
    self.mazzo: mazzo da gioco
    """

    def __init__(self):
        self.carte = []
        self.briscola = None
        self.vincitore = randint(0, 1)
        self.mazzo = Mazzo()

    def Compara(
        self,
    ):
        prima = self.carte[0]
        seconda = self.carte[1]
        if prima.seme == seconda.seme:
            if prima > seconda:
                return 0
            return 1
        if prima.seme == self.briscola.seme:
            return 0
        if seconda.seme == self.briscola.seme:
            return 1
        return 0


class Giocatore:
    def __init__(self):
        self.mano = Mano()
        self.prese = []
        self.punti = 0


class GiocoBriscola:
    """
    Definisce una partita di briscola
    """

    def __init__(self):
        pygame.init()
        self.posizioni = {
            "s0": (62, 282),
            "s1": (182, 282),
            "s2": (302, 282),
            "t0": (122, 62),
            "t1": (242, 62),
            "b": (422, 62),
            "m": (442, 62),
        }
        self.schermata = pygame.display.set_mode((600, 480))
        self.clock = pygame.time.Clock()
        self.down = False
        self.pressed = None

        self.screen = pygame.display.set_mode((600, 480))
        pygame.display.set_caption("eBriscola")
        self.sfondo = pygame.image.load("res" + os.sep + "sfondo.gif")

        self.t1 = SpriteCarta(Carta(0, 11), self.posizioni["t1"])
        self.m = SpriteCarta(Carta(0, 0), self.posizioni["m"])

        # Crea il giocatore umano ed il tavolo
        self.listaGiocatori = [Giocatore(), Giocatore()]
        self.tavolo = Tavolo()
        # Prende la briscola
        self.tavolo.briscola = self.tavolo.mazzo.carte[0]
        self.b = SpriteCarta(self.tavolo.briscola, self.posizioni["b"])
        # Distribuisce carte
        self.tavolo.mazzo.DistribuisciCarte(
            [self.listaGiocatori[0].mano, self.listaGiocatori[1].mano], 6
        )
        # Gioca
        while 1:
            self.GiocaUnaMano()
            if self.listaGiocatori[0].mano.EVuoto():
                break
        self.ContaPunti()
        if self.listaGiocatori[0].punti > self.listaGiocatori[1].punti:
            print(
                " " * 5
                + "%s vince con %i punti"
                % (self.listaGiocatori[0], self.listaGiocatori[0].punti)
            )
            print(
                " " * 5
                + "%s totalizza %i punti"
                % (self.listaGiocatori[1], self.listaGiocatori[1].punti)
            )
        elif self.listaGiocatori[1].punti > self.listaGiocatori[0].punti:
            print(
                " " * 5
                + "%s vince con %i punti"
                % (self.listaGiocatori[1], self.listaGiocatori[1].punti)
            )
            print(
                " " * 5
                + "%s totalizza %i punti"
                % (self.listaGiocatori[0], self.listaGiocatori[0].punti)
            )
        else:
            print(" " * 5 + "La partita finisce patta!")
        self.screen.blit(self.sfondo, (0, 0))
        pygame.display.flip()
        while 1:
            if pygame.event.poll().type == pygame.locals.QUIT:
                sys.exit(0)

    def GiocaUnaMano(self):
        # Scelta della carta e messa sul tavolo
        if len(self.listaGiocatori[0].mano.carte) >= 1:
            self.s0 = SpriteCarta(
                self.listaGiocatori[0].mano.carte[0], self.posizioni["s0"]
            )
        else:
            self.s0 = SpriteCarta(Carta(0, 11), self.posizioni["s0"])
        if len(self.listaGiocatori[0].mano.carte) >= 2:
            self.s1 = SpriteCarta(
                self.listaGiocatori[0].mano.carte[1], self.posizioni["s1"]
            )
        else:
            self.s1 = SpriteCarta(Carta(0, 11), self.posizioni["s1"])
        if len(self.listaGiocatori[0].mano.carte) >= 3:
            self.s2 = SpriteCarta(
                self.listaGiocatori[0].mano.carte[2], self.posizioni["s2"]
            )
        else:
            self.s2 = SpriteCarta(Carta(0, 11), self.posizioni["s2"])
        if self.tavolo.vincitore == 0:
            indiceCartaDaGiocare = self.ScegliCarta()
            cartaDaGiocare = self.listaGiocatori[0].mano.carte.pop(indiceCartaDaGiocare)
            self.tavolo.carte.append(cartaDaGiocare)
            self.t1 = SpriteCarta(cartaDaGiocare, self.posizioni["t1"])
            # Secondo turno
            indiceCartaDaGiocare = randint(0, len(self.listaGiocatori[0].mano.carte))
            cartaDaGiocare = self.listaGiocatori[1].mano.carte.pop(indiceCartaDaGiocare)
            self.tavolo.carte.append(cartaDaGiocare)
            self.t0 = SpriteCarta(cartaDaGiocare, self.posizioni["t0"])

            self.draw()
            self.t0.draw(self.screen)
            pygame.display.flip()
            cur_time = time()
            while time() - cur_time < 1:
                pass
        if self.tavolo.vincitore == 1:
            indiceCartaDaGiocare = randint(
                0, len(self.listaGiocatori[1].mano.carte) - 1
            )
            cartaDaGiocare = self.listaGiocatori[1].mano.carte.pop(indiceCartaDaGiocare)
            self.tavolo.carte.append(cartaDaGiocare)
            self.t0 = SpriteCarta(cartaDaGiocare, self.posizioni["t0"])
            # Secondo turno
            indiceCartaDaGiocare = self.ScegliCarta()
            cartaDaGiocare = self.listaGiocatori[0].mano.carte.pop(indiceCartaDaGiocare)
            self.tavolo.carte.append(cartaDaGiocare)
            self.t1 = SpriteCarta(cartaDaGiocare, self.posizioni["t1"])

            self.draw()
            self.t0.draw(self.screen)
            pygame.display.flip()
            cur_time = time()
            while time() - cur_time < 1:
                pass
        # Chi vince
        self.cartaVincitrice = self.tavolo.Compara()
        self.tavolo.vincitore = (self.tavolo.vincitore + self.cartaVincitrice) % len(
            self.listaGiocatori
        )
        print(
            " " * 5
            + "%s con un %s vince la mano\n"
            % (
                self.listaGiocatori[self.tavolo.vincitore],
                self.tavolo.carte[self.cartaVincitrice],
            )
        )
        # Ultimazioni per riniziare mano
        self.listaGiocatori[self.tavolo.vincitore].prese.extend(self.tavolo.carte)
        self.tavolo.carte[:] = []
        try:
            primaCarta = self.tavolo.mazzo.PrimaCarta()
            self.listaGiocatori[self.tavolo.vincitore].mano.carte.append(primaCarta)
            primaCarta = self.tavolo.mazzo.PrimaCarta()
            self.listaGiocatori[self.tavolo.vincitore - 1].mano.carte.append(primaCarta)
            if indiceCartaDaGiocare == 0:
                s0 = SpriteCarta(primaCarta, self.posizioni["s0"])
            elif indiceCartaDaGiocare == 1:
                s1 = SpriteCarta(primaCarta, self.posizioni["s1"])
            elif indiceCartaDaGiocare == 2:
                s2 = SpriteCarta(primaCarta, self.posizioni["s2"])
        except IndexError:
            pass

    def ScegliCarta(self):
        self.pressed = None
        pressed = None
        while 1:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    sys.exit(0)
                if event.type == pygame.locals.MOUSEBUTTONUP:
                    self.down = False
                    for s, j in [(self.s0, 0), (self.s1, 1), (self.s2, 2)]:
                        if self.t1.rect.colliderect(s):
                            return j
                    for s, j in [(self.s0, "0"), (self.s1, "1"), (self.s2, "2")]:
                        s.rect.topleft = self.posizioni["s" + j]
                if (
                    event.type == pygame.locals.MOUSEBUTTONDOWN
                    and event.button == 1
                    and self.s0.rect.collidepoint(event.pos)
                ):
                    self.down = True
                    pressed = "s0"
                if (
                    event.type == pygame.locals.MOUSEBUTTONDOWN
                    and event.button == 1
                    and self.s1.rect.collidepoint(event.pos)
                ):
                    self.down = True
                    pressed = "s1"
                if (
                    event.type == pygame.locals.MOUSEBUTTONDOWN
                    and event.button == 1
                    and self.s2.rect.collidepoint(event.pos)
                ):
                    self.down = True
                    pressed = "s2"
                if (
                    self.down == True
                    and event.type == pygame.locals.MOUSEMOTION
                    and pressed == "s0"
                ):
                    self.s0.update(event.rel)
                if (
                    self.down == True
                    and event.type == pygame.locals.MOUSEMOTION
                    and pressed == "s1"
                ):
                    self.s1.update(event.rel)
                if (
                    self.down == True
                    and event.type == pygame.locals.MOUSEMOTION
                    and pressed == "s2"
                ):
                    self.s2.update(event.rel)
                pygame.display.flip()
            self.clock.tick(400)

    def draw(self):
        self.screen.blit(self.sfondo, (0, 0))
        if self.pressed != "s0":
            self.s0.draw(self.screen)
        if self.pressed != "s1":
            self.s1.draw(self.screen)
        if self.pressed != "s2":
            self.s2.draw(self.screen)
        if self.tavolo.vincitore == 1:
            self.t0.draw(self.screen)
        # self.t1.draw(self.screen)
        if len(self.tavolo.mazzo.carte) != 0:
            self.b.draw(self.screen)
            self.m.draw(self.screen)
        if self.pressed == "s0":
            self.s0.draw(self.screen)
        if self.pressed == "s1":
            self.s1.draw(self.screen)
        if self.pressed == "s2":
            self.s2.draw(self.screen)

    def ContaPunti(self):
        listaPunteggi = {1: 11, 3: 10, 10: 4, 9: 3, 8: 2}
        for indiceGiocatore in range(len(self.listaGiocatori)):
            for carta in self.listaGiocatori[indiceGiocatore].prese:
                if carta.valore in listaPunteggi.keys():
                    self.listaGiocatori[indiceGiocatore].punti += listaPunteggi[
                        carta.valore
                    ]


if __name__ == "__main__":
    gioco = GiocoBriscola()
