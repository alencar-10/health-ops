from abc import ABC, abstractmethod


class ERPPort(ABC):

    @abstractmethod
    def create_principle(self, codigo, nome, codforma):
        pass

    @abstractmethod
    def create_product(self, codigo, nome):
        pass

    @abstractmethod
    def link_principle(self, product_id, principle_id):
        pass

    @abstractmethod
    def get_product_by_code(self, codigo):
        pass

    @abstractmethod
    def get_principle_by_code(self, codigo):
        pass
