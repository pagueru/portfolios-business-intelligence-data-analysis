// db-vendas-update-marcos-compras.js
db.vendas.updateOne(
        { "nome": "Marcos" },
        {
          $set: {
            "compras": [
              { "nome_produto": "Caderno", "preco": 20.00, "quantidade": 1 },
              { "nome_produto": "Caneta", "preco": 3.00, "quantidade": 5 }
            ]
          }
        }
      )
