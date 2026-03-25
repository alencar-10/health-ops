class PrinciplePayloadBuilder:

    def build(self, codigo, nome, codforma):

        payload = {

            "workMode": "wmInsert",
            "oldWorkMode": "wmBrowse",
            "utf8": "✓",

            "amx_principio_ativo[id]": "",

            "amx_principio_ativo[codprincipio]": codigo,
            "amx_principio_ativo[nomprincipio]": nome,
            "amx_principio_ativo[codforma]": codforma,

            "amx_principio_ativo[indativo]": "S",
            "amx_principio_ativo[indessencial]": "N",
            "amx_principio_ativo[indaltocusto]": "N",
            "amx_principio_ativo[inddiluente]": "N",
        }

        return payload
