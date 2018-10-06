def ler_tokens(): # Leitura de tokens
	lista = []
	while True:
		entrada = input()
		if entrada == '':
			break
		lista.append(entrada)
	return lista

def ler_regras(): # Leitura de expressoes regulares
	lista = []
	while True:
		entrada = input()
		if entrada == '':
			break
		lista.append(entrada)
	return lista

def adicionar_token(aut, token): # Adiciona os tokens no automato
	if(len(aut) == 0): # Cria a regra <S> se o automato esta vazio
		aut.append('<S> ::=')
	for token in tokens: # Adiciona os tokens ao automato
		aux = 0
		for i in token: # Adiciona um simbolo terminal, criando uma nova regra para o proximo simbolo terminal
			aut[aux] += ' ' + i + '<' + str(len(aut)) + '>'
			aux = len(aut)
			aut.append('<' + str(aux) + '> ::=')
	return aut

def adicionar_regras(aut, regras): # Adiciona as regras ao automato
	if(len(aut) == 0): # Cria a regra <S> se o automato esta vazio
		aut.append('<S> ::=')
	for regra in regras: # Adiciona as regras ao automato
		if(regra[1] == 'S'): # Adiciona os simbolos terminais a regra S
			aut[0] += ' ' + regra[8:]
		else: # Adiciona as outras regras no automato
			aut.append(regra)
	return aut

def remover_pipeline(aut): # Remove os pipelines das expressões
	aux = '| '
	a = []
	for i in aut:
		i = i.replace(aux, '')
		a.append(i)
	return a

def formatar(aut):
	aut = remover_pipeline(aut)
	for i in range (0, len(aut)): # Adiciona o simbolo 'ε' para as regras finais
		if aut[i][len(aut[i]) - 1] == '=':
			aut[i] += ' ε'
		aut[i] = aut[i].split()
	return aut

def funcao(aut): #Verifica se não tem uma regra com 'a' e adiciona X. Ex: a = a<X>
	flag = False
	for a in aut:
		for i in range(2, len(a)):
			if len(a[i]) == 1 and a[i] != 'ε':
				a[i] += '<X>'
				flag = True
	if flag and '<X>' not in aut:
		aux = '<X> ::= ε'
		aux = aux.split()
		aut.append(aux)

def add_epTransicao(tabela, transicao, regra):
	flag = False
	for i in range(0 ,len(tabela)):
		if tabela[i][0] == regra:
			for j in range(0, len(tabela)):
				if tabela[j][0] == transicao:
					for t in tabela[j]:
						if t not in tabela[i]:
							tabela[i].append(t)
							flag = True
					break
			break
	return flag

def add_producoes(aut, p1, p2):
	for i in p2[2:]:
		if i not in p1:
			p1.append(i)
	p1.remove(p2[0])
	for i in aut:
		for j in i:
			if j[1:] == p1[0]:
				aux = j[0]+p2[0]
				if aux not in i:
					i.append(j[0]+p2[0])

def copia_producoes(regras, aut):
	for i in aut:
		if i[0] == regras[0]:
			temp = i
			break
	for i in aut:
		for j in regras[1:]:
			if i[0] == j:
				add_producoes(aut, temp, i)

def ep_transicao(aut):
	flag = True
	tabela = []
	aux = 0
	for i in aut:
		temp = []
		temp.append(i[0])
		tabela.append(temp)
	while True:
		flag = False
		for i in aut:
			for j in i[2:]:
				if j[0] == '<':
					if add_epTransicao(tabela, j, i[0]):
						flag = True
						
		if flag == False:
			break
	for i in tabela:
		if len(i) > 1:
			copia_producoes(i, aut)

def get_simbolosTerminais(aut):
	st = []
	for a in aut:
		for i in a[2:]:
			if i == 'ε':
				continue
			if i[0] not in st:
				st.append(i[0])
	return st

def verifica_indeterminizacao(aut, tam, st):
	lista = []
	for a in aut:
		vazia = []
		for i in range (0, tam):
			vazia.append('')
		for i in a[2:]:
			if i == 'ε':
				continue
			indice = st.index(i[0])
			if vazia[indice] != '':
				vazia[indice] += ' '
			vazia[indice] += i[2:-1]
		lista.append(vazia)
	return lista

def existe_regra(regra, aut):
	for a in aut:
		if regra in a[0][1:-1]:
			return True
	return False

def busca_producoes(producoes, aut):
	nova_regra = []
	for p in producoes:
		for a in aut:
			if p == a[0][1:-1] and a[2:]:
				nova_regra.append(a[2:])
	return nova_regra

def add_regra(aut, novas_regras):
	temp = []
	for n in novas_regras:
		aux = n.replace(' ', '')
		aux = '<$' + aux + '> ::='
		producao = n.split()
		regras = busca_producoes(producao, aut)
		aux = aux.split()
		for r in regras:
			for i in r:
				if i not in aux:
					aux.append(i)
		if aux not in aut:
			aut.append(aux)

def remover_itens(aut, itens):
	for i in itens:
		aut.remove(i)

def altera_regra(aut, temp, st):
	for i in range(0, len(temp)):
		for t in temp[i]:
			itens = []
			if ' ' in t:
				indice = temp[i].index(t)
				for j in range(2, len(aut[i])):
					if st[indice] == aut[i][j][0]:
						itens.append(aut[i][j])
				remover_itens(aut[i], itens)

def ordenar(n_regra):
	temp = n_regra.split()
	temp.sort()
	aux = ''
	for i in temp:
		aux += ' '+i;
	return aux

def add_estado(aut, temp, st):
	for i in range(0, len(temp)):
		for t in temp[i]:
			itens = []
			if ' ' in t:
				indice = temp[i].index(t)
				aux = ''
				aux += st[indice]
				aux += '<$'
				t = ordenar(t)
				t = t.replace(' ', '')
				for j in t:
					aux += j
				aux += '>'
				if aux not in aut[i]:
					aut[i].append(aux)

def criar_NovasRegras(aut, temp, st):
	novas_regras = []
	for t in temp:
		for i in t:
			if ' ' in i:
				i = ordenar(i)
				n_regra = i.replace(' ', '')
				if not existe_regra('$'+n_regra ,aut):
					novas_regras.append(i)

	add_regra(aut, novas_regras)
	altera_regra(aut, temp, st)
	add_estado(aut, temp, st)

def determinizacao(aut, lista_temp):
	st = get_simbolosTerminais(aut)
	temp = verifica_indeterminizacao(aut, len(st), st)
	novas_regras = criar_NovasRegras(aut, temp, st)
	if lista_temp != temp:
		determinizacao(aut, temp)

def encontra_producao_terminal(aut):
	for a in aut:
		flag = False
		for i in a[2:]:
			if '*' in i:
				break
			if '<' in i:
				continue
			flag = True
		if flag:
			a.insert(0, '*')

def minimizacao(aut, alcancaveis, indice):
	producao = alcancaveis[indice]
	for a in aut:
		if producao == a[0]:
			for i in a[2:]:
				if len(i) > 2 and i[1:] not in alcancaveis:
					alcancaveis.append(i[1:])

	if len(alcancaveis) > indice + 1:
		minimizacao(aut, alcancaveis, indice + 1)

def add_estado_erro(aut):
	aux = '<-> ::='
	aux = aux.split()
	aut.append(aux)

def remover_producoes_inalcancaveis(aut, alcancaveis):
	for i in range (len(aut) - 1, 0, -1):
		if aut[i][0] not in alcancaveis:
			aut.remove(aut[i])
	add_estado_erro(aut)

def EstMortos(aut, mortos, p):
	if p in mortos:
		mortos.remove(p)
	for i in aut:
		for j in i:
			if j[1:] == p and i[0] in mortos:
				EstMortos(aut, mortos, i[0])


def busca_EstMortos(aut):
	producoes = []
	producoesTerminais = []
	mortos = []
	for i in aut:
		for j in i:
			if len(j) == 3 and j != '::=' and j not in producoes:
				producoes.append(j)
			elif len(j) > 3 and j[0] != '<' and j[1:] not in producoes:
				producoes.append(j[1:])
		if 'ε' in i or i[0] == '<->':
			producoesTerminais.append(i[0])
	mortos = producoes.copy()
	for i in producoesTerminais:
		if i in mortos:
			mortos.remove(i)
	for i in producoesTerminais:
		if i != '<->':
			EstMortos(aut, mortos, i)
	return mortos

def removerMortos(aut, mortos):
	for i in range(len(aut) - 1, -1, -1):
		if aut[i][0] in mortos:
			print(i)
			aut.pop(i)
			continue
		for j in range(len(aut[i]) - 1, -1, -1):
			if aut[i][j][1:] in mortos:
				aut[i].pop(j)

def print_Automato(aut):
	st = get_simbolosTerminais(aut)
	for a in aut:
		aux = a[0] + a[1] 
		for i in st:
			aux += ' ' + i
			flag = ''
			for j in a:
				if i == j[0]:
					flag = j[1:] + ' '
			if flag != '':
				aux += flag
			else:
				aux += '<->'
		if 'ε' in a:
			aux += ' ε'
		aux = aux.replace('  ', ' ')
		aux = aux.replace('> ', '> | ')
		aux = aux.replace('>::', '> ::')
		print(aux)

tokens = ler_tokens()
regras = ler_regras()
automato = []
automato = adicionar_token(automato, tokens)
automato = adicionar_regras(automato, regras)
automato = formatar(automato)
funcao(automato)
#Encontrar e remover as epslon transiçoes: Criar tabela, Copiar os estados, Dulplicar: bS -> bA para que S ::= A
ep_transicao(automato);
temp = []
determinizacao(automato, temp)
alcancaveis = ['<S>']
minimizacao(automato, alcancaveis, 0)
remover_producoes_inalcancaveis(automato, alcancaveis)
mortos = busca_EstMortos(automato)
removerMortos(automato, mortos)
print_Automato(automato)