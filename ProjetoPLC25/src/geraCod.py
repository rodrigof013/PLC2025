from Erros import Erros

class GeraCod:
    def __init__(self,ast,simb):
        self.ast=ast
        self.tSimb=simb
        self.lCod = []
        self.labelCounter=0

    def gera_codigo(self):
        self.emit(f'//{self.ast.get('nome','')}')
        self._abreEspacio()
        self.emit('jump main')
        self._trata_funcoes()
        self.emit('')
        self.emit('main:')
        self.emit('start')
        self._trata_main()
        self.emit('stop')
        return '\n'.join(self.lCod)

    def emit(self, instrucao, name=None):
        comentario = f' // {name}' if name else ''
        self.lCod.append(f'{instrucao}{comentario}')

    def _new_label(self, prefix='L'):
        self.labelCounter += 1
        return f"{prefix}{self.labelCounter}"

    def gera_expressao(self, exp, funcao_atual=None):
        if not exp: return

        tipo = exp.get('tipo')

        if tipo == 'LITERAL':
            val = exp['valor']
            datatype = exp['datatype']
            
            if datatype == 'integer':
                self.emit(f"pushi {val}")
            elif datatype == 'real':
                self.emit(f"pushf {val}")
            elif datatype == 'string':
                self.emit(f'pushs "{val}"')
            elif datatype == 'char':
                self.emit(f'pushi {ord(val)}')
            elif datatype == 'boolean':
                val_int = 1 if val else 0
                self.emit(f"pushi {val_int}")
            return datatype

        if tipo in ['VAR', 'ARRAY_ACCESS', 'FIELD_ACCESS']:
            return self._gerar_acesso_var_load(exp, funcao_atual)

        if tipo == 'CALL':
            return self._gerar_chamada(exp, funcao_atual)

        if 'op' in exp and 'left' in exp:
            op = exp['op'].upper()
            
            t_left = self.gera_expressao(exp['left'], funcao_atual)
            t_right = self.gera_expressao(exp['right'], funcao_atual)
            
            if t_left == 'real' and t_right == 'integer':
                self.emit("itof")
                t_right = 'real'
            elif t_left == 'integer' and t_right == 'real':
                self.emit("swap")
                self.emit("itof")
                self.emit("swap")
                t_left = 'real'
            
            is_float = (t_left == 'real' or t_right == 'real')
            
            if op == '+': 
                self.emit("fadd" if is_float else "add")
                return 'real' if is_float else 'integer'
            elif op == '-': 
                self.emit("fsub" if is_float else "sub")
                return 'real' if is_float else 'integer'
            elif op == '*': 
                self.emit("fmul" if is_float else "mul")
                return 'real' if is_float else 'integer'
            elif op == '/':
                if not is_float:
                    self.emit("itof")
                    self.emit("swap")
                    self.emit("itof")
                    self.emit("swap")
                self.emit("fdiv")
                return 'real'
            elif op == 'DIV':
                self.emit("div")
                return 'integer'
            elif op == 'MOD':
                self.emit("mod")
                return 'integer'

            elif op in ['=', 'EQUAL']: 
                self.emit("fequal" if is_float else "equal")
                return 'boolean'
            elif op in ['<>', 'NE', 'NEQ']: 
                self.emit("fequal" if is_float else "equal")
                self.emit("not")
                return 'boolean'
            elif op in ['<', 'LT', 'LESS']: 
                self.emit("finf" if is_float else "inf")
                return 'boolean'
            elif op in ['>', 'GT', 'GREAT']: 
                self.emit("fsup" if is_float else "sup")
                return 'boolean'
            elif op in ['<=', 'LE', 'LEQ']: 
                self.emit("finfeq" if is_float else "infeq")
                return 'boolean'
            elif op in ['>=', 'GE', 'GEQ']: 
                self.emit("fsupeq" if is_float else "supeq")
                return 'boolean'
            
            elif op == 'AND': 
                self.emit("and")
                return 'boolean'
            elif op == 'OR': 
                self.emit("or")
                return 'boolean'
            
            return t_left 

        if 'op' in exp and 'right' in exp:
            op = exp['op'].upper()
            tipo_right=self.gera_expressao(exp['right'], funcao_atual)
            
            if op == '-': 
                if tipo_right == 'integer':
                    self.emit('pushi 0')
                    self.emit('swap')
                    self.emit('sub')
                elif tipo_right == 'real':
                    self.emit('pushf 0.0')
                    self.emit('swap')
                    self.emit('fsub')
                return tipo_right
            elif op == 'NOT': 
                self.emit("not")
            
            return

    def _extrair_referencia(self, exp):
        indices = []
        fields = []
        current = exp
        
        while True:
            if current.get('tipo') == 'FIELD_ACCESS':
                fields.insert(0, current.get('field'))
                current = current.get('target', {})
            elif current.get('tipo') == 'ARRAY_ACCESS':
                curr_inds = current.get('indices', [])
                indices = curr_inds + indices
                current = current.get('target', {})
            else:
                break
        
        return indices, fields, current
    
    def _gerar_acesso_var_load(self, exp, funcao_atual):
        indices, fields, var_node = self._extrair_referencia(exp)
        nome_var = var_node.get('nome', '')
        
        if funcao_atual and nome_var in self.tSimb.get(funcao_atual, {}).get('vars', {}):
            info_var = self.tSimb[funcao_atual]['vars'][nome_var]
            is_local = True
        elif nome_var in self.tSimb:
            info_var = self.tSimb[nome_var]
            is_local = False
        else:
            print(Erros.get('ger', exp.get('linha'), 'VAR_N_EXISTE', nome=nome_var))
            return None
        
        sp = info_var.get('sp', 0)
        tipo_info = info_var.get('tipo', {})
        tipo_base = tipo_info.get('tipo', 'atomico')
        is_string = tipo_info.get('is_string', False)
        
        if is_string and indices:
            instrucao = 'pushl' if is_local else 'pushg'
            self.emit(f'{instrucao} {sp}')
            
            self.gera_expressao(indices[0], funcao_atual)
            dim = tipo_info.get('dimensoes', [{}])[0]
            min_val = dim.get('min', 1)
            if min_val != 0:
                self.emit(f'pushi {min_val}')
                self.emit('sub')
            
            self.emit('charat')
            return 'char'
        
        if is_string and not indices:
            instrucao = 'pushl' if is_local else 'pushg'
            self.emit(f'{instrucao} {sp}')
            return 'string'
        
        if not indices and not fields and tipo_base in ['array', 'record']:
            if is_local:
                self.emit('pushfp')
                self.emit(f'pushi {sp}')
                self.emit('padd')
            else:
                self.emit('pushgp')
                self.emit(f'pushi {sp}')
                self.emit('padd')
            return 'address'
        
        if not indices and not fields:
            instrucao = 'pushl' if is_local else 'pushg'
            self.emit(f'{instrucao} {sp}')
            if tipo_info.get('tipo') == 'atomico':
                return tipo_info.get('nome', 'integer')
            return tipo_info.get('tipo', 'integer')
        
        if is_local:
            self.emit('pushfp')
            self.emit(f'pushi {sp}')
            self.emit('padd')
        else:
            self.emit('pushgp')
            self.emit(f'pushi {sp}')
            self.emit('padd')
        
        tipo_atual = tipo_info
        
        if indices:
            dimensoes = tipo_info.get('dimensoes', [])
            
            for i, idx_exp in enumerate(indices):
                self.gera_expressao(idx_exp, funcao_atual)
                
                dim = dimensoes[i] if i < len(dimensoes) else {'min': 0, 'max': 0}
                min_val = dim.get('min', 0)
                if min_val != 0:
                    self.emit(f'pushi {min_val}')
                    self.emit('sub')
                
                tamanho_restante = 1
                for j in range(i + 1, len(dimensoes)):
                    d = dimensoes[j]
                    tamanho_restante *= (d.get('max', 0) - d.get('min', 0) + 1)
                
                if tamanho_restante != 1:
                    self.emit(f'pushi {tamanho_restante}')
                    self.emit('mul')
                
                self.emit('padd')
            
            tipo_atual = tipo_info.get('of', {})
        
        if fields:
            for field_name in fields:
                campos = tipo_atual.get('campos', [])
                campo_info = None
                for c in campos:
                    if c['nome'] == field_name:
                        campo_info = c
                        break
                
                if campo_info:
                    offset = campo_info.get('offset', 0)
                    if offset != 0:
                        self.emit(f'pushi {offset}')
                        self.emit('padd')
                    tipo_atual = campo_info.get('tipo', {})
                else:
                    print(Erros.get('ger', None, 'CAMPO_N_EXISTE', nome=field_name))
                    return None

        self.emit('load 0')
        
        if isinstance(tipo_atual, dict):
            if tipo_atual.get('tipo') == 'atomico':
                return tipo_atual.get('nome', 'integer')
            return tipo_atual.get('tipo', 'integer')
        return 'integer'

    def _extrair_fields(self, exp):
        fields = []
        current = exp
        
        while current.get('tipo') == 'FIELD_ACCESS':
            fields.insert(0, current.get('field'))
            current = current.get('target', {})
        
        return fields, current

    def _extrair_indices(self, exp):
        indices = []
        current = exp
        
        while current.get('tipo') == 'ARRAY_ACCESS':
            current_indices = current.get('indices', [])
            indices = current_indices + indices
            current = current.get('target', {})
        
        return indices, current

    def _gerar_chamada(self, exp, funcao_atual):
        nome = exp['nome']
        args = exp.get('args', [])
        
        func_info = self.tSimb.get(nome, {})
        has_return = func_info.get('categoria') == 'func'
        
        for arg in args:
            self.gera_expressao(arg, funcao_atual)
        
        self.emit(f'pusha {nome}')
        self.emit('call')
        
        num_args = len(args)
        
        if has_return and num_args > 0:
            for _ in range(num_args):
                self.emit('swap')
                self.emit('pop 1')
        elif not has_return and num_args > 0:
            self.emit(f'pop {num_args}')
        
        ret_tipo = func_info.get('return', {})
        if ret_tipo:
            if isinstance(ret_tipo, dict):
                if ret_tipo.get('tipo') == 'atomico':
                    return ret_tipo.get('nome', 'integer')
                return ret_tipo.get('tipo', 'integer')
            return ret_tipo
        return None

    def _abreEspacioPrimitivo(self,tipo,name):
        jbb=tipo.get('nome',tipo.get('datatype','nada'))
        if jbb=='char':
            self.emit('pushs ""',name)
        elif jbb=='integer':
            self.emit('pushi 0',name)
        elif jbb=='real':
            self.emit('pushf 0',name)
        elif jbb=='boolean':
            self.emit('pushi 0',name)
        else:
            print(Erros.get('ger', None, 'TIPO_N_IMPLEMENTADO', nome=tipo.get('nome', 'desconhecido')))

    def _abreEspacio(self):
        vars_globais = [(k, v) for k, v in self.tSimb.items() if v.get('categoria') == 'var']
        vars_globais.sort(key=lambda x: x[1].get('sp', 0))
        
        for k, v in vars_globais:
            tipo = v['tipo']
            dtt = tipo['tipo']
            if dtt in ['atomico','subrange']:
                self._abreEspacioPrimitivo(tipo,k)
            elif dtt in ['array','record']:
                self.emit(f"pushn {tipo['size']}",k)
            elif dtt == 'enum':
                self.emit('pushs ""',k)

    def gera_instrucao(self, stmt, funcao_atual=None):
        if not stmt:
            return
        
        tipo = stmt.get('tipo')
        
        if tipo == 'BLOCO':
            for s in stmt.get('instrucoes', []):
                self.gera_instrucao(s, funcao_atual)

        elif tipo == 'LABEL':
            self.emit('')
            self.emit(f'{stmt.get('label')}:')
            self.gera_instrucao(stmt.get('instrucao'),funcao_atual)

        elif tipo == 'GOTO':
            self.emit(f'jump {stmt.get('label')}')
        
        elif tipo == 'ATRIBUICAO':
            target = stmt.get('var')
            value = stmt.get('val')
            self.gera_expressao(value, funcao_atual)
            self._gerar_acesso_var_store(target, funcao_atual)
        
        elif tipo == 'IF':
            cond = stmt.get('cond')
            then_branch = stmt.get('then')
            else_branch = stmt.get('else')
            
            if else_branch:
                label_else = self._new_label('ELSE')
                label_end = self._new_label('ENDIF')
                
                self.gera_expressao(cond, funcao_atual)
                self.emit(f'jz {label_else}')
                self.gera_instrucao(then_branch, funcao_atual)
                self.emit(f'jump {label_end}')
                self.emit('')
                self.emit(f'{label_else}:')
                self.gera_instrucao(else_branch, funcao_atual)
                self.emit('')
                self.emit(f'{label_end}:')
            else:
                label_end = self._new_label('ENDIF')
                
                self.gera_expressao(cond, funcao_atual)
                self.emit(f'jz {label_end}')
                self.gera_instrucao(then_branch, funcao_atual)
                self.emit('')
                self.emit(f'{label_end}:')
        
        elif tipo == 'WHILE':
            label_start = self._new_label('WHILE')
            label_end = self._new_label('ENDWHILE')
            
            self.emit('')
            self.emit(f'{label_start}:')
            self.gera_expressao(stmt.get('cond'), funcao_atual)
            self.emit(f'jz {label_end}')
            self.gera_instrucao(stmt.get('do'), funcao_atual)
            self.emit(f'jump {label_start}')
            self.emit('')
            self.emit(f'{label_end}:')
        
        elif tipo == 'REPEAT':
            label_start = self._new_label('REPEAT')
            
            self.emit('')
            self.emit(f'{label_start}:')
            for s in stmt.get('instrucoes', []):
                self.gera_instrucao(s, funcao_atual)
            self.gera_expressao(stmt.get('until'), funcao_atual)
            self.emit(f'jz {label_start}')
        
        elif tipo == 'FOR':
            nome_var = stmt.get('var')
            start_val = stmt.get('inicio')
            end_val = stmt.get('fim')
            body = stmt.get('do')
            passo = stmt.get('passo', 'TO').upper()
            
            var_node = {'tipo': 'VAR', 'nome': nome_var}
            
            label_start = self._new_label('FOR')
            label_end = self._new_label('ENDFOR')
            
            self.gera_expressao(start_val, funcao_atual)
            self._gerar_acesso_var_store(var_node, funcao_atual)
            
            self.emit('')
            self.emit(f'{label_start}:')
            
            self.gera_expressao(var_node, funcao_atual)
            self.gera_expressao(end_val, funcao_atual)
            if passo == 'TO':
                self.emit('infeq')
            else:
                self.emit('supeq')
            self.emit(f'jz {label_end}')
            
            self.gera_instrucao(body, funcao_atual)
            
            self.gera_expressao(var_node, funcao_atual)
            self.emit('pushi 1')
            if passo == 'TO':
                self.emit('add')
            else:
                self.emit('sub')
            self._gerar_acesso_var_store(var_node, funcao_atual)
            
            self.emit(f'jump {label_start}')
            self.emit('')
            self.emit(f'{label_end}:')
        
        elif tipo == 'CASE':
            expr = stmt.get('exp')
            cases = stmt.get('cases', [])
            label_end = self._new_label('ENDCASE')
            
            for case in cases:
                if case is None:
                    continue
                label_next = self._new_label('CASE')
                labels = case.get('labels', [])
                
                if len(labels) == 1:
                    self.gera_expressao(expr, funcao_atual)
                    self.gera_expressao(labels[0], funcao_atual)
                    self.emit('equal')
                else:
                    for i, lbl in enumerate(labels):
                        self.gera_expressao(expr, funcao_atual)
                        self.gera_expressao(lbl, funcao_atual)
                        self.emit('equal')
                        if i > 0:
                            self.emit('or')
                
                self.emit(f'jz {label_next}')
                self.gera_instrucao(case.get('instrucao'), funcao_atual)
                self.emit(f'jump {label_end}')
                self.emit('')
                self.emit(f'{label_next}:')
            
            self.emit('')
            self.emit(f'{label_end}:')
        
        elif tipo == 'CALL':
            self._gerar_chamada(stmt, funcao_atual)
        
        elif tipo == 'WRITE':
            args = stmt.get('args', [])
            for arg in args:
                exp = arg.get('exp', arg)
                tipo_arg = self.gera_expressao(exp, funcao_atual)
                if tipo_arg == 'integer':
                    self.emit('writei')
                elif tipo_arg == 'real':
                    self.emit('writef')
                elif tipo_arg == 'string':
                    self.emit('writes')
                elif tipo_arg == 'boolean':
                    self.emit('writei')
                elif tipo_arg == 'char':
                    self.emit('writechr')
                else:
                    self.emit('writei')
            
            if stmt.get('newline', False):
                self.emit('writeln')
        
        elif tipo == 'READ':
            args = stmt.get('args', [])
            for arg in args:
                nome_var = arg.get('nome', '')
                tipo_var = self._obter_tipo_var(nome_var, funcao_atual)
                
                if tipo_var == 'real':
                    self.emit('read')
                    self.emit('atof')
                    self._gerar_acesso_var_store(arg, funcao_atual)
                elif tipo_var == 'string':
                    self.emit('read')
                    self._gerar_acesso_var_store(arg, funcao_atual)
                elif tipo_var == 'char':
                    self.emit('read')
                    self.emit('chrcode')
                    self._gerar_acesso_var_store(arg, funcao_atual)
                else:
                    self.emit('read')
                    self.emit('atoi')
                    self._gerar_acesso_var_store(arg, funcao_atual)

    def _obter_tipo_var(self, nome_var, funcao_atual):
        if funcao_atual and nome_var in self.tSimb.get(funcao_atual, {}).get('vars', {}):
            info = self.tSimb[funcao_atual]['vars'][nome_var]
        elif nome_var in self.tSimb:
            info = self.tSimb[nome_var]
        else:
            return 'integer'
        
        tipo_info = info.get('tipo', {})
        if tipo_info.get('tipo') == 'atomico':
            return tipo_info.get('nome', 'integer')
        if tipo_info.get('tipo') == 'array':
            tipo_of = tipo_info.get('of', {})
            if tipo_of.get('nome') == 'char':
                return 'string'
        return 'integer'

    def _gerar_endereco_var(self, exp, funcao_atual):
        nome_var = exp.get('nome', '')
        
        if funcao_atual and nome_var in self.tSimb.get(funcao_atual, {}).get('vars', {}):
            info_var = self.tSimb[funcao_atual]['vars'][nome_var]
            is_local = True
        elif nome_var in self.tSimb:
            info_var = self.tSimb[nome_var]
            is_local = False
        else:
            print(Erros.get('ger', None, 'VAR_N_EXISTE', nome=nome_var))
            return
        
        sp = info_var.get('sp', 0)
        
        if is_local:
            self.emit('pushfp')
            self.emit(f'pushi {sp}')
            self.emit('padd')
        else:
            self.emit('pushgp')
            self.emit(f'pushi {sp}')
            self.emit('padd')

    def _gerar_acesso_var_store(self, exp, funcao_atual):
        indices, fields, var_node = self._extrair_referencia(exp)
        nome_var = var_node.get('nome', '')
        
        if funcao_atual and nome_var in self.tSimb.get(funcao_atual, {}).get('vars', {}):
            info_var = self.tSimb[funcao_atual]['vars'][nome_var]
            is_local = True
        elif nome_var in self.tSimb:
            info_var = self.tSimb[nome_var]
            is_local = False
        else:
            print(Erros.get('ger',exp.get('linha'), 'VAR_N_EXISTE', nome=nome_var))
            return
        
        sp = info_var.get('sp', 0)
        tipo_info = info_var.get('tipo', {})
        
        if not indices and not fields:
            instrucao = 'storel' if is_local else 'storeg'
            self.emit(f'{instrucao} {sp}')
            return
        
        if is_local:
            self.emit('pushfp')
            self.emit(f'pushi {sp}')
            self.emit('padd')
        else:
            self.emit('pushgp')
            self.emit(f'pushi {sp}')
            self.emit('padd')
        
        tipo_atual = tipo_info
        
        if indices:
            dimensoes = tipo_info.get('dimensoes', [])
            
            for i, idx_exp in enumerate(indices):
                self.gera_expressao(idx_exp, funcao_atual)
                
                dim = dimensoes[i] if i < len(dimensoes) else {'min': 0, 'max': 0}
                min_val = dim.get('min', 0)
                if min_val != 0:
                    self.emit(f'pushi {min_val}')
                    self.emit('sub')
                
                tamanho_restante = 1
                for j in range(i + 1, len(dimensoes)):
                    d = dimensoes[j]
                    tamanho_restante *= (d.get('max', 0) - d.get('min', 0) + 1)
                
                if tamanho_restante != 1:
                    self.emit(f'pushi {tamanho_restante}')
                    self.emit('mul')
                
                self.emit('padd')
            
            tipo_atual = tipo_info.get('of', {})
        
        if fields:
            for field_name in fields:
                campos = tipo_atual.get('campos', [])
                campo_info = None
                for c in campos:
                    if c['nome'] == field_name:
                        campo_info = c
                        break
                
                if campo_info:
                    offset = campo_info.get('offset', 0)
                    if offset != 0:
                        self.emit(f'pushi {offset}')
                        self.emit('padd')
                    tipo_atual = campo_info.get('tipo', {})
        
        self.emit('swap')
        self.emit('store 0')

    def _trata_funcoes(self):
        decl_list = self.ast.get('decl', [])
        
        for decl_block in decl_list:
            if decl_block.get('tipo') != 'DECL_ROTINAS':
                continue
            
            for func in decl_block.get('vals', []):
                nome = func['nome']
                info = self.tSimb.get(nome, {})
                
                self.emit('')
                self.emit(f'{nome}:')
                
                vars_locais = info.get('vars', {})
                espaco_local = 0
                for var_nome, var_info in vars_locais.items():
                    if var_info.get('sp', 0) >= 0:
                        tipo_var = var_info.get('tipo', {})
                        if tipo_var.get('tipo') in ['array', 'record']:
                            espaco_local += tipo_var.get('size', 1)
                        else:
                            espaco_local += 1
                
                if espaco_local > 0:
                    self.emit(f'pushn {espaco_local}')
                
                corpo = func.get('corpo', [])
                for inst in corpo:
                    self.gera_instrucao(inst, nome)
                
                if info.get('categoria') == 'func':
                    if nome in vars_locais:
                        ret_sp = vars_locais[nome].get('sp', 0)
                        self.emit(f'pushl {ret_sp}')
                        if espaco_local > 0:
                            for _ in range(espaco_local):
                                self.emit('swap')
                                self.emit('pop 1')
                        self.emit('return')
                    else:
                        if espaco_local > 0:
                            self.emit(f'pop {espaco_local}')
                        self.emit('return')
                else:
                    if espaco_local > 0:
                        self.emit(f'pop {espaco_local}')
                    self.emit('return')

    def _trata_main(self):
        instrucoes = self.ast.get('main', [])
        for inst in instrucoes:
            self.gera_instrucao(inst)
