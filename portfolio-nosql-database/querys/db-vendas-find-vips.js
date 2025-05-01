// db-vendas-find-vips.js
db.vendas.find({ "vip": 1 }, { "nome": 1, "_id": 0 }).pretty()
