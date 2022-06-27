library(tidyr)
library(ggplot2)

testes <- c("test02", "test03", "test04", "test08", "test09", "test13")

tempos <- function() {
	read.csv("benchmarks/tempos.csv", row.names = NULL) |> subset(Teste %in% testes) |>
		pivot_longer(2:5, names_to = "Algoritmo", values_to = "Tempo") |>
		ggplot(aes(x = Teste, y = Tempo, fill = Algoritmo)) +
		geom_col(position="dodge") + coord_flip() + scale_x_discrete(limits=rev) +
		labs(x = "Teste", y = "Tempo [ms]")

	ggsave("benchmarks/tempos.png", device="png", height = 4, width = 6.5, dpi = 600)
}

expandidos <- function() {
	read.csv("benchmarks/expandidos.csv", row.names = NULL) |> subset(Teste %in% testes) |>
		pivot_longer(2:5, names_to = "Algoritmo", values_to = "Nós Expandidos") |>
		ggplot(aes(x = Teste, y = `Nós Expandidos`, fill = Algoritmo)) +
		geom_col(position="dodge") + coord_flip() + scale_x_discrete(limits=rev)

	ggsave("benchmarks/expandidos.png", device="png", height = 4, width = 6.5, dpi = 600)
}

gerados <- function() {
	read.csv("benchmarks/gerados.csv", row.names = NULL) |> subset(Teste %in% testes) |>
		pivot_longer(2:5, names_to = "Algoritmo", values_to = "Nós Gerados") |>
		ggplot(aes(x = Teste, y = `Nós Gerados`, fill = Algoritmo)) +
		geom_col(position="dodge") + coord_flip() + scale_x_discrete(limits=rev)

	ggsave("benchmarks/gerados.png", device="png", height = 4, width = 6.5, dpi = 600)
}

tempos()
expandidos()
gerados()
