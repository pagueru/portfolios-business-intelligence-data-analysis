// db-vendas-aggregate-produtos-distintos.js
db.vendas.aggregate([
      { $unwind: "$compras" },
      { $group: { _id: "$compras.nome_produto" } },
      { $project: { "nome_produto": "$_id", "_id": 0 } }
    ]).pretty()
