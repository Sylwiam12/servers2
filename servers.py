#!/usr/bin/python
# -*- coding: utf-8 -*-
# Sylwia Michalska , 407870 Julia Midera , 407628 Paweł Mitręga ,406867
from abc import ABC, abstractmethod
from typing import Optional, List, Union
import re


def is_name_valid(name):
    def is_letter(sign):
        if (ord('a') <= ord(sign) <= ord('z')) or (ord('A') <= ord(sign) <= ord('Z')):
            return True
        else:
            return False

    def is_number(sign):
        if ord('0') <= ord(sign) <= ord('9'):
            return True
        else:
            return False

    n_count = 0
    l_count = 0
    letters_part = True
    for sign in name:
        if (not is_number(sign)) and (not is_letter(sign)):
            raise ValueError('Name can only consist of letter and numbers')
        if letters_part and is_number(sign):
            letters_part = False
        if not letters_part and is_letter(sign):
            raise ValueError('Cannot place letter after number')
        if is_number(sign):
            n_count += 1
        if is_letter(sign):
            l_count += 1
    if l_count == 0 or n_count == 0:
        raise ValueError('name must consist of at least 1 number and 1 letter')


def is_price_valid(price):
    if price < 0:
        raise ValueError('cena jest mniejsza od zera')


class Product:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str) i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)

    def __init__(self, name: str, price: float):
        is_name_valid(name)
        is_price_valid(price)
        self.name = name
        self.price = price

    def __eq__(self, other):
        return (self.name == other.name) and (self.price == other.price)  # FIXME: zwróć odpowiednią wartość

    def __hash__(self):
        return hash((self.name, self.price))


class TooManyProductsFoundError(Exception):
    pass


class Server(ABC):  # klasa abstrakcyjna

    def __init__(self):
        super().__init__()

    n_max_returned_entries = 4
    products = None

    def get_entries(self, n_letters: int = 1) -> List[Product]:
        criteria = "[a-zA-Z]" + "{" + str(n_letters) + "}[1-9]{2,3}"
        list = []
        for i in self._get_all_products(n_letters):
            if re.match(criteria, i.name):
                list.append(i)
            if len(list) > Server.n_max_returned_entries:
                raise TooManyProductsFoundError(len(list), self.n_max_returned_entries)
        if len(list) > Server.n_max_returned_entries:
            raise TooManyProductsFoundError(len(list), self.n_max_returned_entries)
        list.sort(key=lambda entry: entry.price)
        return list

    @abstractmethod
    def _get_all_products(self, n_letters: int = 1) -> List[Product]:
        raise NotImplementedError


# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania

class ListServer(Server):
    products = []

    def __init__(self, products):
        super().__init__()
        self.products = products

    def _get_all_products(self, n_letters: int = 1) -> List[Product]:
        return self.products


class MapServer(Server):
    products = {}

    def __init__(self, products):
        super().__init__()
        for product in products:
            self.products[product.name] = product

    def _get_all_products(self, n_letters: int = 1) -> List[Product]:
        product_list = []
        for key in self.products.keys():
            product_list.append(self.products[key])
        return product_list


class Client:
    def __init__(self, server):
        self.client_server = server

    def get_total_price(self, n_letters: int):
        try:
            products = self.client_server.get_entries(n_letters)
        except:
            return None
        else:
            sum_price = 0
            if products:
                for product in products:
                    sum_price = sum_price + product.price
                return sum_price
            else:
                return None
