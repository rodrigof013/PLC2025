from Erros import Erros

class AnalisadorSemantico:
    def __init__(self):
        self.tabela_simbolos = {} 
        self.erros = []
        self.sp = 0

    def adicionar_erro(self, linha, mensagem, **kwargs):
        msg=Erros.get('sem',linha,mensagem,**kwargs)
        if msg:
            self.erros.append(msg)
            print(msg)

    def _resolver_valor(self, nodo):
        if not isinstance(nodo, dict): return nodo
        
        if nodo.get('datatype') == 'id':
            nome = nodo['valor']
            if nome in self.tabela_simbolos:
                simb = self.tabela_simbolos[nome]
                if simb['categoria'] == 'const':
                    return simb['valor']
                else:
                    self.adicionar_erro(0, 'VAR_N_EXISTE', nome=nome)
                    return 0
            else:
                self.adicionar_erro(0, 'VAR_N_EXISTE', nome=nome)
                return 0
        
        try:
            return int(nodo['valor'])
        except ValueError:
            if isinstance(nodo['valor'], str) and len(nodo['valor']) == 1:
                return ord(nodo['valor'])
            return nodo['valor']

    def _processar_tipo(self, ast_tipo):
        if isinstance(ast_tipo, str):
            if ast_tipo in self.tabela_simbolos:
                return self.tabela_simbolos[ast_tipo].copy()
            return {'tipo': 'atomico', 'nome': ast_tipo, 'size': 1}

        tipo = ast_tipo['tipo']

        if tipo == 'SUBRANGE':
            v_min = self._resolver_valor(ast_tipo['min'])
            v_max = self._resolver_valor(ast_tipo['max'])
            datatype = ast_tipo['min'].get('datatype', 'INTEGER') 
            return {
                'tipo': 'subrange',
                'min': v_min,
                'max': v_max,
                'datatype': datatype,
                'size': 1
            }

        elif tipo == 'ENUM':
            return {
                'tipo': 'enum',
                'vals': ast_tipo['vals'],
                'size': 1
            }

        elif tipo == 'ARRAY':
            tipo_base = self._processar_tipo(ast_tipo['of'])
            total_size = tipo_base['size']
            dimensoes = []

            for indice in ast_tipo['indices']:
                if isinstance(indice, str):
                     info_idx = self._processar_tipo(indice)
                     if info_idx['tipo'] == 'subrange':
                         tamanho_dim = info_idx['max'] - info_idx['min'] + 1
                     elif info_idx['tipo'] == 'enum':
                         tamanho_dim = len(info_idx['vals'])
                     else:
                         tamanho_dim = 1
                     total_size *= tamanho_dim
                     dimensoes.append(info_idx)
                else:
                    info_idx = self._processar_tipo(indice)
                    tamanho_dim = info_idx['max'] - info_idx['min'] + 1
                    total_size *= tamanho_dim
                    dimensoes.append(info_idx)

            is_packed_string = ast_tipo.get('packed', False) and tipo_base.get('nome') == 'char'
            
            return {
                'tipo': 'array',
                'dimensoes': dimensoes,
                'of': tipo_base,
                'size': 1 if is_packed_string else total_size,
                'packed': ast_tipo.get('packed', False),
                'is_string': is_packed_string
            }

        elif tipo == 'RECORD':
            campos = []
            offset_atual = 0
            
            for campo_ast in ast_tipo['campos']:
                if campo_ast is None: continue
                
                tipo_campo = self._processar_tipo(campo_ast['tipo'])
                lista_nomes = campo_ast.get('vars', campo_ast.get('ids', []))
                
                for nome_id in lista_nomes:
                    campos.append({
                        'nome': nome_id,
                        'tipo': tipo_campo,
                        'offset': offset_atual
                    })
                    offset_atual += tipo_campo['size']

            return {
                'tipo': 'record',
                'campos': campos,
                'size': offset_atual
            }
        
        return {'tipo': 'unknown', 'size': 0}

    def realizar_analise(self, ast):
        self.initTabela(ast)

        if ast and 'decl' in ast and isinstance(ast['decl'], list):
            blocos_rotins = filter(lambda x: x['tipo'] == 'DECL_ROTINAS', ast['decl'])
            for bloco in blocos_rotins:
                for rotina in bloco['vals']:
                    self.check_instrucoes(rotina['corpo'], rotina['nome'])

        if ast and 'main' in ast:
            self.check_instrucoes(ast['main'], None)

        return self.tabela_simbolos

    def initTabela(self,ast):
        if ast is None:
            return
        if isinstance(ast,dict):
            self.insLabels(ast['decl'])
            self.insConsts(ast['decl'])
            self.insTypes(ast['decl'])
            self.insVars(ast['decl'])
            self.insRotins(ast['decl'])

    def insLabels(self, ast):
        if ast is None:
            return
        if isinstance(ast, list):
            blocos_labels = filter(lambda x: x['tipo'] == 'DECL_LABELS', ast)
            for bl in blocos_labels:
                for label in bl['vals']:
                    if label in self.tabela_simbolos:
                        self.adicionar_erro(0, 'VAR_EXISTE', nome=label)
                    else:
                        self.tabela_simbolos[label] = {'tipo': 'label'}
        
    def insConsts(self,ast):
        if ast is None:
            return
        if isinstance(ast,list):
            blocos_const=filter(lambda x: x['tipo']=='DECL_CONSTS',ast)
            for bl in blocos_const:
                for const in bl['vals']:
                    if const['tipo']=='DEF_CONST':
                        if const['nome'] in self.tabela_simbolos:
                            self.adicionar_erro('Declarações','CONST_EXISTE',nome=const['nome'])
                            return
                        else:
                            self.tabela_simbolos[const['nome']]={}
                            self.tabela_simbolos[const['nome']]['categoria'] = 'const'
                            self.tabela_simbolos[const['nome']]['datatype'] = const['val']['datatype']

    def insTypes(self,ast):
        if ast is None:
            return
        if isinstance(ast,list):
            blocos_types=filter(lambda x: x['tipo']=='DECL_TYPES',ast)
            for bl in blocos_types:
                for tp in bl['vals']:
                    if tp['tipo'] == 'DEF_TYPE':
                        nome = tp['nome']
                        info_tipo = self._processar_tipo(tp['val'])
                        info_tipo['categoria'] = 'type'
                        
                        if nome in self.tabela_simbolos:
                            self.adicionar_erro(0, 'VAR_EXISTE', nome=nome)
                        else:
                            self.tabela_simbolos[nome] = info_tipo

    def insVars(self, ast, func=False, initial_scope=None):
        vars_locais = initial_scope.copy() if initial_scope else {}
        spLocal=0
        if ast is None: 
            return vars_locais
        
        if isinstance(ast, list):
            blocos_vars = filter(lambda x: x['tipo'] == 'DECL_VARS', ast)
            
            for bl in blocos_vars:
                for var in bl['vals']:
                    if var['tipo'] == 'DECL_VAR':
                        info_tipo = self._processar_tipo(var['datatype'])
                        nomes = var['nomes']
                        
                        for nm in nomes:
                            onde_verificar = vars_locais if func else self.tabela_simbolos
                            
                            if nm in onde_verificar:
                                self.adicionar_erro(0, 'VAR_EXISTE', nome=nm)
                            else:
                                entrada = {
                                    'categoria': 'var_local' if func else 'var',
                                    'tipo': info_tipo
                                }
                                
                                if func:
                                    entrada['sp'] = spLocal
                                    spLocal += 1
                                    vars_locais[nm] = entrada
                                else:
                                    entrada['sp'] = self.sp
                                    self.tabela_simbolos[nm] = entrada
                                    self.sp += info_tipo['size']
                                    
        return vars_locais

    def insRotins(self, ast):
        if ast is None:
            return
        
        if isinstance(ast, list):
            blocos_rotins = filter(lambda x: x['tipo'] == 'DECL_ROTINAS', ast)
            for bloco in blocos_rotins:
                for fun in bloco['vals']:
                    spLocal = -1
                    nome_func = fun['nome']
                    
                    if nome_func in self.tabela_simbolos:
                        self.adicionar_erro(0, 'VAR_EXISTE', nome=nome_func)
                        continue

                    args = []
                    args_dict = {}
                    
                    for param in fun['params']:
                        tipo_param = self._processar_tipo(param['tipo'])
                        lista_nomes = param.get('vars', param.get('ids', []))
                        
                        for var in lista_nomes:
                            if var in args_dict:
                                self.adicionar_erro(0, 'VAR_EXISTE', nome=var)
                            
                            size_param = tipo_param.get('size', 1)
                            spLocal -= (size_param - 1)
                            
                            arg_entry = {
                                'nome': var,
                                'tipo': tipo_param,
                                'categoria': 'param',
                                'sp': spLocal
                            }
                            spLocal -= 1
                            args.append(arg_entry)
                            args_dict[var] = arg_entry

                    retorno = None
                    if fun['tipo'] == 'FUNCTION':
                        retorno = self._processar_tipo(fun.get('val', fun.get('retrn',fun.get('return'))))

                    vars_locais = self.insVars(fun['decl'], func=True, initial_scope=args_dict)

                    if fun['tipo'] == 'FUNCTION' and retorno:
                        max_sp = -1
                        for var_info in vars_locais.values():
                            var_sp = var_info.get('sp', -1)
                            if var_sp >= 0:
                                var_size = var_info.get('tipo', {}).get('size', 1)
                                max_sp = max(max_sp, var_sp + var_size - 1)
                        
                        ret_sp = max_sp + 1
                        vars_locais[nome_func] = {
                            'tipo': retorno,
                            'categoria': 'return',
                            'sp': ret_sp
                        }

                    self.tabela_simbolos[nome_func] = {
                        'categoria': 'void' if fun['tipo'] == 'PROCEDURE' else 'func',
                        'args': args,
                        'vars': vars_locais,
                        'return': retorno
                    }

    def check_instrucoes(self,ast,funcao=None):
        if not ast:
            return
        
        for inst in ast:
            if inst is None: continue
            tipo = inst['tipo']
            if tipo == 'ATRIBUICAO':
                self.check_atribuicao(inst, funcao)
            elif tipo == 'IF':
                self.check_if(inst,funcao)
            elif tipo == 'WHILE':
                self.check_while(inst,funcao)
            elif tipo == 'REPEAT':
                self.check_repeat(inst, funcao)
            elif tipo == 'FOR':
                self.check_for(inst, funcao)
            elif tipo == 'BLOCO':
                self.check_instrucoes(inst['instrucoes'], funcao)
            elif tipo == 'CALL':
                self.check_proc(inst, funcao)
            elif tipo == 'READ':
                self.check_read(inst, funcao)
            elif tipo == 'WRITE':
                self.check_write(inst, funcao)
            elif tipo == 'CASE':
                self.check_case(inst, funcao)
            elif tipo == 'GOTO':
                self.check_goto(inst, funcao)
            elif tipo == 'LABEL':
                self.check_label(inst, funcao)

    def check_label(self, inst, funcao=None):
        label = inst['label']
        if label not in self.tabela_simbolos:
             self.adicionar_erro(inst['linha'], 'VAR_N_EXISTE', nome=f"Label {label}")
        elif self.tabela_simbolos[label]['tipo'] != 'label':
             self.adicionar_erro(inst['linha'], 'TIPO_INCOMPATIVEL', esperado='Label', recebido=self.tabela_simbolos[label]['tipo'])
        self.check_instrucoes([inst['instrucao']], funcao)

    def check_read(self, inst, funcao=None):
        for arg in inst['args']:
            if arg['tipo'] not in ['VAR', 'ARRAY_ACCESS', 'FIELD_ACCESS']:
                 self.adicionar_erro(inst['linha'], 'TIPO_INCOMPATIVEL', esperado='Variavel', recebido='Expressao')
                 continue
            
            tipo_var_dict = self._get_tipo_variavel(arg, funcao)
            if not tipo_var_dict: continue

            nome_tipo = tipo_var_dict['nome'] if tipo_var_dict['tipo'] == 'atomico' else tipo_var_dict['tipo']
            
            if nome_tipo not in ['integer', 'real', 'char', 'string']:
                 if tipo_var_dict['tipo'] == 'array' and tipo_var_dict['of']['nome'] == 'char' and tipo_var_dict['packed']:
                     pass
                 else:
                     self.adicionar_erro(inst['linha'], 'TIPO_INCOMPATIVEL', esperado='Tipo Leitura (int, real, char, string)', recebido=nome_tipo)

    def check_write(self, inst, funcao=None):
        for item in inst['args']:
            tipo_exp = self.check_exp(item['exp'], funcao)
            if not tipo_exp: continue
            
            if tipo_exp not in ['integer', 'real', 'char', 'string', 'boolean']:
                 self.adicionar_erro(inst['linha'], 'TIPO_INCOMPATIVEL', esperado='Tipo Escrita', recebido=tipo_exp)

    def check_case(self, inst, funcao=None):
        tipo_exp = self.check_exp(inst['exp'], funcao)
        if not tipo_exp: return

        if tipo_exp == 'real':
             self.adicionar_erro(inst['linha'], 'TIPO_INCOMPATIVEL', esperado='Ordinal', recebido='real')
        
        if inst['cases']:
            for case in inst['cases']:
                for label in case['labels']:
                    tipo_label = label['datatype']
                    if tipo_label != tipo_exp:
                         self.adicionar_erro(inst['linha'], 'TIPO_INCOMPATIVEL', esperado=tipo_exp, recebido=tipo_label)
                self.check_instrucoes([case['instrucao']], funcao)

    def check_goto(self, inst, funcao=None):
        label = str(inst['label'])
        if label not in self.tabela_simbolos:
             self.adicionar_erro(inst['linha'], 'VAR_N_EXISTE', nome=f"Label {label}")
        elif self.tabela_simbolos[label]['tipo'] != 'label':
             self.adicionar_erro(inst['linha'], 'TIPO_INCOMPATIVEL', esperado='Label', recebido=self.tabela_simbolos[label]['tipo'])

    def check_proc(self, inst, funcao=None):
        nome = inst['nome']
        if nome in self.tabela_simbolos:
            sym = self.tabela_simbolos[nome]
            if sym['categoria'] != 'void':
                self.adicionar_erro(inst.get('linha', 0), 'TIPO_INCOMPATIVEL', esperado='Procedimento', recebido=sym['categoria'])
                return
            
            args_decl = sym.get('args', [])
            args_call = inst.get('args', [])

            if len(args_decl) != len(args_call):
                self.adicionar_erro(inst.get('linha', 0), 'NUM_ARGS', nome=nome, esperado=len(args_decl), recebido=len(args_call))
            else:
                for i, arg_call in enumerate(args_call):
                    tipo_arg_call = self.check_exp(arg_call, funcao)
                    arg_decl = args_decl[i]
                    tipo_arg_decl = arg_decl['tipo']
                    
                    nome_tipo_esperado = 'unknown'
                    if tipo_arg_decl['tipo'] == 'atomico':
                        nome_tipo_esperado = tipo_arg_decl['nome']
                    else:
                        nome_tipo_esperado = tipo_arg_decl['tipo']

                    if tipo_arg_call != nome_tipo_esperado:
                        if nome_tipo_esperado == 'real' and tipo_arg_call == 'integer':
                            pass
                        else:
                            self.adicionar_erro(inst.get('linha', 0), 'ARG_TIPO', 
                                              param=arg_decl['nome'], 
                                              esperado=nome_tipo_esperado, 
                                              recebido=tipo_arg_call)
        else:
            self.adicionar_erro(inst.get('linha', 0), 'FUNCAO_NAO_DECLARADA', nome=nome)

    def _get_tipo_variavel(self, exp, nome_funcao=None):
        if exp['tipo'] == 'VAR':
            nome_var = exp['nome']
            
            if nome_funcao and nome_var == nome_funcao:
                if nome_funcao in self.tabela_simbolos:
                    sym = self.tabela_simbolos[nome_funcao]
                    if sym['categoria'] == 'func':
                        return sym['return']

            simbolo = None

            if nome_funcao and nome_funcao in self.tabela_simbolos:
                func_entry = self.tabela_simbolos[nome_funcao]
                if 'vars' in func_entry and nome_var in func_entry['vars']:
                    simbolo = func_entry['vars'][nome_var]
                elif 'args' in func_entry:
                    for arg in func_entry['args']:
                        if arg['nome'] == nome_var:
                            simbolo = arg
                            break
            
            if not simbolo and nome_var in self.tabela_simbolos:
                simbolo = self.tabela_simbolos[nome_var]
    
            if not simbolo:
                self.adicionar_erro(exp.get('linha', 0), 'VAR_N_EXISTE', nome=nome_var)
                return None
            
            return simbolo['tipo']

        elif exp['tipo'] == 'ARRAY_ACCESS':
            tipo_alvo = self._get_tipo_variavel(exp['target'], nome_funcao)
            
            if not tipo_alvo: return None

            if tipo_alvo['tipo'] != 'array':
                self.adicionar_erro(exp.get('linha', 0), 'TIPO_INCOMPATIVEL', esperado='Array', recebido=tipo_alvo['tipo'])
                return None
            
            indices = exp.get('indices', [exp['index']] if 'index' in exp else [])
            
            for indice in indices:
                tipo_idx = self.check_exp(indice, nome_funcao)
                if tipo_idx != 'integer':
                    self.adicionar_erro(exp.get('linha', 0), 'TIPO_INCOMPATIVEL', 
                                      esperado='integer', recebido=tipo_idx)

            num_indices = len(indices)
            num_dimensoes = len(tipo_alvo.get('dimensoes', []))
            
            if num_indices >= num_dimensoes:
                return tipo_alvo['of']
            else:
                return {
                    'tipo': 'array',
                    'dimensoes': tipo_alvo['dimensoes'][num_indices:],
                    'of': tipo_alvo['of'],
                    'size': tipo_alvo['size'],
                    'packed': tipo_alvo.get('packed', False)
                }

        elif exp['tipo'] == 'FIELD_ACCESS':
            tipo_alvo = self._get_tipo_variavel(exp['target'], nome_funcao)
            
            if not tipo_alvo: return None

            if tipo_alvo['tipo'] != 'record':
                self.adicionar_erro(exp.get('linha', 0), 'TIPO_INCOMPATIVEL', esperado='Record', recebido=tipo_alvo['tipo'])
                return None

            nome_campo = exp['field']
            for campo in tipo_alvo['campos']:
                if campo['nome'] == nome_campo:
                    return campo['tipo']
            
            self.adicionar_erro(exp.get('linha', 0), 'VAR_N_EXISTE', nome=f"Campo '{nome_campo}'")
            return None

    def check_exp(self, exp, funcao=None):
        if not exp: return None

        if exp['tipo'] == 'LITERAL':
            return exp['datatype']

        if exp['tipo'] in ['VAR', 'ARRAY_ACCESS', 'FIELD_ACCESS']:
            tipo_d = self._get_tipo_variavel(exp, funcao)
            if not tipo_d: return None
            if tipo_d['tipo'] == 'atomico':
                return tipo_d['nome']
            else:
                return tipo_d['tipo']

        if exp['tipo'] == 'CALL':
            nome = exp['nome']
            if nome in self.tabela_simbolos:
                sym = self.tabela_simbolos[nome]
                if sym['categoria'] != 'func':
                    self.adicionar_erro(exp.get('linha', 0), 'TIPO_INCOMPATIVEL', esperado='Função', recebido=sym['categoria'])
                    return None
                
                args_decl = sym.get('args', [])
                args_call = exp.get('args', [])

                if len(args_decl) != len(args_call):
                    self.adicionar_erro(exp.get('linha', 0), 'NUM_ARGS', nome=nome, esperado=len(args_decl), recebido=len(args_call))
                else:
                    for i, arg_call in enumerate(args_call):
                        tipo_arg_call = self.check_exp(arg_call, funcao)
                        arg_decl = args_decl[i]
                        tipo_arg_decl = arg_decl['tipo']
                        
                        nome_tipo_esperado = 'unknown'
                        if tipo_arg_decl['tipo'] == 'atomico':
                            nome_tipo_esperado = tipo_arg_decl['nome']
                        else:
                            nome_tipo_esperado = tipo_arg_decl['tipo']

                        if tipo_arg_call != nome_tipo_esperado:
                            if nome_tipo_esperado == 'real' and tipo_arg_call == 'integer':
                                pass
                            else:
                                self.adicionar_erro(exp.get('linha', 0), 'ARG_TIPO', 
                                                  param=arg_decl['nome'], 
                                                  esperado=nome_tipo_esperado, 
                                                  recebido=tipo_arg_call)

                return sym['return']['nome'] 
            else:
                self.adicionar_erro(exp.get('linha', 0), 'FUNCAO_NAO_DECLARADA', nome=nome)
                return None

        if 'right' in exp and 'left' not in exp:
            op = exp['op']
            t_right = self.check_exp(exp['right'], funcao)
            
            if op in ['NOT','not']:
                if t_right != 'boolean':
                    self.adicionar_erro(0, 'TIPO_INCOMPATIVEL', esperado='boolean', recebido=t_right)
                return 'boolean'
            elif op in ['+', '-']:
                if t_right not in ['integer', 'real']:
                    self.adicionar_erro(0, 'TIPO_INCOMPATIVEL', esperado='numero', recebido=t_right)
                return t_right

        if 'op' in exp:
            op = exp['op']
            t_left = self.check_exp(exp['left'], funcao)
            t_right = self.check_exp(exp['right'], funcao)

            if t_left is None or t_right is None:
                return None

            if op in ['+', '-', '*']:
                if t_left == 'integer' and t_right == 'integer':
                    return 'integer'
                elif t_left in ['integer', 'real'] and t_right in ['integer', 'real']:
                    return 'real'
                else:
                    self.adicionar_erro(0, 'TIPO_INCOMPATIVEL', esperado='numero', recebido=f"{t_left} {op} {t_right}")
                    return None

            elif op == '/':
                if t_left in ['integer', 'real'] and t_right in ['integer', 'real']:
                    return 'real'
                else:
                    self.adicionar_erro(0, 'TIPO_INCOMPATIVEL', esperado='numero', recebido=f"{t_left} / {t_right}")
                    return None

            elif op in ['div', 'mod','DIV','MOD']:
                if t_left == 'integer' and t_right == 'integer':
                    return 'integer'
                else:
                    self.adicionar_erro(0, 'TIPO_INCOMPATIVEL', esperado='integer', recebido=f"{t_left} {op} {t_right}")
                    return None

            elif op in ['AND', 'OR','and','or']:
                if t_left == 'boolean' and t_right == 'boolean':
                    return 'boolean'
                else:
                    self.adicionar_erro(0, 'TIPO_INCOMPATIVEL', esperado='boolean', recebido=f"{t_left} {op} {t_right}")
                    return None

            elif op in ['>', '<', '>=', '<=', '=', '<>', 'NE', 'GE', 'LE']:
                if t_left == t_right:
                    return 'boolean'
                elif t_left in ['integer', 'real'] and t_right in ['integer', 'real']:
                    return 'boolean'
                else:
                    self.adicionar_erro(0, 'TIPO_INCOMPATIVEL', esperado='tipos compativeis', recebido=f"{t_left} vs {t_right}")
                    return None

        return None
        
    def check_atribuicao(self, inst, funcao=None):
        tipo_var = self._get_tipo_variavel(inst['var'], funcao)
        tipo_exp = self.check_exp(inst['val'], funcao)

        if not tipo_var or not tipo_exp:
            return 

        nome_tipo_var = tipo_var
        if isinstance(tipo_var, dict):
            nome_tipo_var = tipo_var.get('nome', tipo_var.get('tipo'))

        nome_tipo_exp = tipo_exp
        if isinstance(tipo_exp, dict):
             nome_tipo_exp = tipo_exp.get('nome', tipo_exp.get('tipo'))

        if nome_tipo_var == nome_tipo_exp:
            return
        elif nome_tipo_var == 'real' and nome_tipo_exp == 'integer':
            return
        else:
            self.adicionar_erro(inst['linha'], 'TIPO_INCOMPATIVEL', 
                            esperado=nome_tipo_var, 
                            recebido=nome_tipo_exp)

    def check_if(self, inst, funcao=None):
        cond_type = self.check_exp(inst['cond'], funcao)
        if cond_type != 'boolean':
            self.adicionar_erro(inst['linha'], 'TIPO_INCOMPATIVEL', esperado='boolean', recebido=cond_type)
        
        if inst['then']:
            self.check_instrucoes([inst['then']], funcao)
        if inst['else']:
            self.check_instrucoes([inst['else']], funcao)

    def check_while(self, inst, funcao=None):
        cond_type = self.check_exp(inst['cond'], funcao)
        if cond_type != 'boolean':
            self.adicionar_erro(inst['linha'], 'TIPO_INCOMPATIVEL', esperado='boolean', recebido=cond_type)
        
        if inst['do']:
            self.check_instrucoes([inst['do']], funcao)

    def check_repeat(self, inst, funcao=None):
        cond_type = self.check_exp(inst['until'], funcao)
        if cond_type != 'boolean':
            self.adicionar_erro(inst['linha'], 'TIPO_INCOMPATIVEL', esperado='boolean', recebido=cond_type)
        
        if inst['instrucoes']:
            self.check_instrucoes(inst['instrucoes'], funcao)

    def check_for(self, inst, funcao=None):
        nome_var = inst['var']
        var_node = {'tipo': 'VAR', 'nome': nome_var, 'linha': inst['linha']}
        tipo_var_dict = self._get_tipo_variavel(var_node, funcao)
        
        if not tipo_var_dict: return

        if tipo_var_dict['tipo'] != 'atomico':
             self.adicionar_erro(inst['linha'], 'TIPO_INCOMPATIVEL', esperado='Tipo Simples', recebido=tipo_var_dict['tipo'])
             return
        
        nome_tipo = tipo_var_dict['nome']

        t_inicio = self.check_exp(inst['inicio'], funcao)
        t_fim = self.check_exp(inst['fim'], funcao)

        if t_inicio != nome_tipo:
            self.adicionar_erro(inst['linha'], 'TIPO_INCOMPATIVEL', esperado=nome_tipo, recebido=t_inicio)
        
        if t_fim != nome_tipo:
            self.adicionar_erro(inst['linha'], 'TIPO_INCOMPATIVEL', esperado=nome_tipo, recebido=t_fim)

        if inst['do']:
            self.check_instrucoes([inst['do']], funcao)
