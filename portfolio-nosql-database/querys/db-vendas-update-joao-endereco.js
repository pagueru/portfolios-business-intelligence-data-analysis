// db-vendas-update-joao-endereco.js
db.vendas.updateOne(
      { "nome": "João" },
      {
        $set: {
          "endereco": {
            "rua": "Rua Um",
            "numero": 1000,
            "complemento": "Apto 1 Bloco 1",
            "cidade": "São Paulo",
            "estado": "SP"
          }
        }
      }
    )
