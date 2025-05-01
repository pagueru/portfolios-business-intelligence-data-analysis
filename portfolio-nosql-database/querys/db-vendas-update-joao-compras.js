// db-vendas-update-joao-compras.js
db.vendas.updateOne(
      { "nome": "João" },
      {
        $set: {
          "compras": [
            { "nome_produto": "notebook", "preco": 5000.00, "quantidade": 1 }
          ]
        }
      }
    )
