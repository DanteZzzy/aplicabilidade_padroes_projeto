from abc import ABC, abstractmethod

class AgendamentoRepositoryInterface(ABC):
    
    @abstractmethod
    def salvar_agendamento(self, cliente: str, data_hora, metodo_pagamento: str, valor_total: float, servicos: list):
        pass
    
    @abstractmethod
    def verificar_horario_existente(self, data_hora) -> bool:
        pass