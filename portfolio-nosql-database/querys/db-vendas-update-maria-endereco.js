// db-vendas-update-maria-endereco.js
db.vendas.updateOne(
      { "nome": "Maria" },
      {
        $set: {
          "endereco": {
            "rua": "Rua Três",
            "numero": 3000,
            "cidade": "Londrina",
            "estado": "PR"
          }
        }
      }
    )
