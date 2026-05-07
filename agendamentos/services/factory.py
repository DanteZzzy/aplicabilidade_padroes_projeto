from agendamentos.models import Servico


class ServiceFactory:

    @staticmethod
    def criar_servicos_padrao():

        servicos = [

            {
                "nome": "Corte Social",
                "tipo": "corte",
                "preco": 25
            },

            {
                "nome": "Corte Degradê",
                "tipo": "corte",
                "preco": 30
            },

            {
                "nome": "Barba",
                "tipo": "barba",
                "preco": 20
            },

            {
                "nome": "Barba (com toalha quente)",
                "tipo": "barba",
                "preco": 25
            }
        ]

        for servico in servicos:

            Servico.objects.get_or_create(

                nome=servico["nome"],

                defaults={
                    "tipo": servico["tipo"],
                    "preco": servico["preco"]
                }
            )