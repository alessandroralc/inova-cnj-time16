# Contributing

Para a melhor participação de todos, gentileza seguir as práticas descritas abaixo e que são pontuadas para o desafio:


## Padrão de commits:
Devemos utilizar o padrão descrito no link [convetional commits]:https://www.conventionalcommits.org/en/v1.0.0-beta.2/ 
A seguir um pequeno resumo.
O commit deve seguir o padrão:

```
<type>[optional scope]: <description>

[optional body]

[optional footer]
```
Abaixo o domínio válido para o <type>:
1. fix: Sempre que for uma correção de erro
1. feat: Nova funcionalidade do tipo MINOR
1. BREAKING CHANGE: Nova funcionalidade do tipo MAJOR (pode ser utilizada no body)
1. Others: Para commits que sejam diferentes de fix: and feat: vamos teremos os demais tipos a seguir: `chore:, docs:, style:, refactor:, perf:, test:, and others.`

O *scope* é opcional para o commit, mas pode enriquecer adicionando informação contextual

Exemplos de commits:

### Commit de uma nova funcionalidade com o *BREAKING CHANGE* no body

```
feat: allow provided config object to extend other configs

BREAKING CHANGE: `extends` key in config file is now used for extending other config files
```

### Commit sem body

```
docs: correct spelling of CHANGELOG
```

### Commit com a utilização de escopo

```
feat(lang): added polish language
```
