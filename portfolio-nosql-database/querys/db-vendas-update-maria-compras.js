// db-vendas-update-maria-compras.js
db.vendas.updateOne(
        { "nome": "Maria" },
        {
          $set: {
            "compras": [
              { "nome_produto": "Borracha", "preco": 2.00, "quantidade": 2 },
              { "nome_produto": "Tablet", "preco": 2500.00, "quantidade": 1 },
              { "nome_produto": "Capa para tablet", "preco": 50.00, "quantidade": 1 }
            ]
          }
        }
      )
